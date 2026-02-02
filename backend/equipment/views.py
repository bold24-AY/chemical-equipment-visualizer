"""
API Views for Equipment Dataset Management.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import Dataset
from .serializers import DatasetSerializer, DatasetSummarySerializer
from .utils import validate_csv_structure, analyze_csv, get_chart_data

# PDF generation imports
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Polygon, Circle
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend

import io
from datetime import datetime


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Simple username/password authentication.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'message': 'Login successful',
            'username': user.username
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout current user.
    """
    logout(request)
    return Response({'message': 'Logout successful'})

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.
    """
    from .serializers import UserSerializer
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user) # Auto-login after registration
        return Response({
            'message': 'User registered successfully',
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth(request):
    """
    Check if user is authenticated.
    """
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'username': request.user.username
        })
    return Response({'authenticated': False})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """
    Upload and process CSV file.
    Validates structure, analyzes data, and stores in database.
    Maintains only last 5 uploads for the current user.
    """
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Validate file type
    if not file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate CSV structure
    is_valid, error_message = validate_csv_structure(file)
    if not is_valid:
        return Response(
            {'error': error_message},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Reset file pointer after validation
    file.seek(0)
    
    # Analyze CSV
    try:
        summary, raw_data = analyze_csv(file)
    except Exception as e:
        return Response(
            {'error': f'Error analyzing CSV: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Create dataset record
    dataset = Dataset.objects.create(
        user=request.user,
        file_name=file.name,
        summary=summary,
        raw_data=raw_data
    )
    
    # Keep only last 5 uploads for this user
    ids_to_keep = list(Dataset.objects.filter(user=request.user).order_by('-uploaded_at').values_list('id', flat=True)[:5])
    if ids_to_keep:
        Dataset.objects.filter(user=request.user).exclude(id__in=ids_to_keep).delete()
    
    serializer = DatasetSerializer(dataset)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request):
    """
    Get the most recent dataset summary for the current user.
    """
    try:
        latest_dataset = Dataset.objects.filter(user=request.user).first()
        if not latest_dataset:
            return Response(
                {'error': 'No datasets uploaded yet'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = DatasetSerializer(latest_dataset)
        return Response(serializer.data)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """
    Get last 5 dataset uploads for the current user.
    """
    datasets = Dataset.objects.filter(user=request.user)[:5]
    serializer = DatasetSummarySerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset(request, dataset_id):
    """
    Get specific dataset by ID (ensuring it belongs to the user).
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request, dataset_id=None):
    """
    Generate PDF report for a dataset.
    """
    try:
        # Get dataset
        if dataset_id:
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        else:
            dataset = Dataset.objects.filter(user=request.user).first()
            if not dataset:
                return Response(
                    {'error': 'No datasets available'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # --- Logo ---
        logo_drawing = Drawing(40, 40)
        points = [20, 40, 37, 30, 37, 10, 20, 0, 3, 10, 3, 30]
        hexagon = Polygon(points)
        hexagon.fillColor = colors.HexColor('#1a5490')
        hexagon.strokeColor = colors.HexColor('#1a5490')
        logo_drawing.add(hexagon)
        
        circle = Circle(20, 20, 10)
        circle.fillColor = colors.white
        circle.strokeColor = colors.white
        logo_drawing.add(circle)
        
        story.append(logo_drawing)
        story.append(Spacer(1, 0.1*inch))
        
        # --- Title ---
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=20,
            alignment=1  # Center
        )
        story.append(Paragraph("Chemical Equipment Parameter Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # --- Metadata ---
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555')
        )
        story.append(Paragraph(f"<b>Dataset:</b> {dataset.file_name}", info_style))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))
        story.append(Paragraph(f"<b>Uploaded:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", info_style))
        story.append(Spacer(1, 0.3*inch))
        
        # --- Summary Statistics Table ---
        story.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        summary = dataset.summary
        
        # Helper to safely get value
        def get_val(key, fmt="{:.2f}"):
            val = summary.get(key)
            if val is None:
                return "N/A"
            return fmt.format(val)

        summary_data = [
            ['Metric', 'Value', 'Min', 'Max'],
            ['Total Equipment', str(summary.get('total_equipment', 0)), '-', '-'],
            ['Flowrate', get_val('average_flowrate'), get_val('min_flowrate'), get_val('max_flowrate')],
            ['Pressure', get_val('average_pressure'), get_val('min_pressure'), get_val('max_pressure')],
            ['Temperature', get_val('average_temperature'), get_val('min_temperature'), get_val('max_temperature')],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'), # Left align first column
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f2f6')]),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.2*inch))
        
        # --- Bar Chart ---
        bar_elements = []
        bar_elements.append(Paragraph("<b>Average Parameters</b>", styles['Heading2']))
        bar_elements.append(Spacer(1, 0.1*inch))
        
        drawing = Drawing(450, 200)
        bar_chart = VerticalBarChart()
        bar_chart.x = 50
        bar_chart.y = 50
        bar_chart.height = 150
        bar_chart.width = 350
        bar_chart.data = [[
            summary.get('average_flowrate', 0),
            summary.get('average_pressure', 0),
            summary.get('average_temperature', 0)
        ]]
        bar_chart.categoryAxis.categoryNames = ['Flowrate', 'Pressure', 'Temperature']
        bar_chart.bars[0].fillColor = colors.HexColor('#1a5490')
        bar_chart.valueAxis.valueMin = 0
        drawing.add(bar_chart)
        bar_elements.append(drawing)
        
        story.append(KeepTogether(bar_elements))
        story.append(Spacer(1, 0.2*inch))
        
        # --- Pie Chart ---
        pie_elements = []
        pie_elements.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
        pie_elements.append(Spacer(1, 0.1*inch))
        
        pie_drawing = Drawing(450, 250)
        pie = Pie()
        pie.x = 20
        pie.y = 60
        pie.width = 150
        pie.height = 150
        
        # Data
        labels = list(summary['type_distribution'].keys())
        data = list(summary['type_distribution'].values())
        
        pie.data = data
        pie.labels = None # Disable direct labels to avoid overlap
        
        # Colors
        pie_colors = [
            colors.HexColor('#1a5490'), colors.HexColor('#4a69bd'),
            colors.HexColor('#6a89cc'), colors.HexColor('#82ccdd'),
            colors.HexColor('#b8e994'), colors.HexColor('#f8c291'),
            colors.HexColor('#e55039')
        ]
        
        for i, val in enumerate(pie.data):
             pie.slices[i].fillColor = pie_colors[i % len(pie_colors)]
             pie.slices[i].strokeColor = colors.white
             pie.slices[i].strokeWidth = 1
        
        pie_drawing.add(pie)
        
        # Legend
        legend = Legend()
        legend.x = 220
        legend.y = 160
        legend.boxAnchor = 'w'
        legend.columnMaximum = 10
        legend.fontName = 'Helvetica'
        legend.fontSize = 10
        
        # Create color/name pairs for legend
        legend_data = []
        for i, label in enumerate(labels):
            color = pie_colors[i % len(pie_colors)]
            # Add count to label
            label_text = f"{label} ({data[i]})"
            legend_data.append((color, label_text))
            
        legend.colorNamePairs = legend_data
        pie_drawing.add(legend)
        
        pie_elements.append(pie_drawing)
        story.append(KeepTogether(pie_elements))
        
        # --- Build PDF ---
        doc.build(story)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
        return response
    
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error generating report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
