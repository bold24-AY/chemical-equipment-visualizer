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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Polygon, Circle
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie

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
    Maintains only last 5 uploads.
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
        file_name=file.name,
        summary=summary,
        raw_data=raw_data
    )
    
    # Keep only last 5 uploads
    ids_to_keep = list(Dataset.objects.order_by('-uploaded_at').values_list('id', flat=True)[:5])
    if ids_to_keep:
        Dataset.objects.exclude(id__in=ids_to_keep).delete()
    
    serializer = DatasetSerializer(dataset)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request):
    """
    Get the most recent dataset summary.
    """
    try:
        latest_dataset = Dataset.objects.first()
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
    Get last 5 dataset uploads (summary only, no raw data).
    """
    datasets = Dataset.objects.all()[:5]
    serializer = DatasetSummarySerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset(request, dataset_id):
    """
    Get specific dataset by ID.
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id)
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
    Includes summary statistics and charts.
    """
    try:
        # Get dataset
        if dataset_id:
            dataset = Dataset.objects.get(id=dataset_id)
        else:
            dataset = Dataset.objects.first()
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
        
        # Logo - Simple Chemical Benzene Ring
        logo_drawing = Drawing(40, 40)
        # Hexagon points
        points = [20, 40, 37, 30, 37, 10, 20, 0, 3, 10, 3, 30]
        hexagon = Polygon(points)
        hexagon.fillColor = colors.HexColor('#1a5490')
        hexagon.strokeColor = colors.HexColor('#1a5490')
        logo_drawing.add(hexagon)
        
        # Circle inside (aromatic ring)
        circle = Circle(20, 20, 10)
        circle.fillColor = colors.white
        circle.strokeColor = colors.white
        logo_drawing.add(circle)
        
        story.append(logo_drawing)
        story.append(Spacer(1, 0.1*inch))
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("Chemical Equipment Parameter Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Dataset Info
        info_style = styles['Normal']
        story.append(Paragraph(f"<b>Dataset:</b> {dataset.file_name}", info_style))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))
        story.append(Paragraph(f"<b>Uploaded:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", info_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Summary Statistics Table
        story.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        summary = dataset.summary
        summary_data = [
            ['Metric', 'Value'],
            ['Total Equipment', str(summary['total_equipment'])],
            ['Average Flowrate', f"{summary['average_flowrate']:.2f}"],
            ['Average Pressure', f"{summary['average_pressure']:.2f}"],
            ['Average Temperature', f"{summary['average_temperature']:.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Equipment Type Distribution Table
        story.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        type_data = [['Equipment Type', 'Count']]
        for eq_type, count in summary['type_distribution'].items():
            type_data.append([eq_type, str(count)])
        
        type_table = Table(type_data, colWidths=[3*inch, 2*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(type_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Bar Chart - Average Parameters
        story.append(Paragraph("<b>Average Parameters Chart</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        drawing = Drawing(400, 200)
        bar_chart = VerticalBarChart()
        bar_chart.x = 50
        bar_chart.y = 50
        bar_chart.height = 125
        bar_chart.width = 300
        bar_chart.data = [[
            summary['average_flowrate'],
            summary['average_pressure'],
            summary['average_temperature']
        ]]
        bar_chart.categoryAxis.categoryNames = ['Flowrate', 'Pressure', 'Temperature']
        bar_chart.bars[0].fillColor = colors.HexColor('#1a5490')
        drawing.add(bar_chart)
        story.append(drawing)
        story.append(Spacer(1, 0.3*inch))
        
        # Pie Chart - Equipment Type Distribution
        story.append(Paragraph("<b>Equipment Type Distribution Chart</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        pie_drawing = Drawing(400, 200)
        pie = Pie()
        pie.x = 150
        pie.y = 50
        pie.width = 100
        pie.height = 100
        pie.data = list(summary['type_distribution'].values())
        pie.labels = list(summary['type_distribution'].keys())
        pie.slices.strokeWidth = 0.5
        pie_drawing.add(pie)
        story.append(pie_drawing)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Return PDF response
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
