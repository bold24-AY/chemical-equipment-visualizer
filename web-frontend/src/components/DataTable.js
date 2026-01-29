import React from 'react';

function DataTable({ data }) {
  if (!data || data.length === 0) {
    return <div className="no-data">No equipment data available.</div>;
  }

  return (
    <div className="data-table-container">
      <h2>Equipment Data</h2>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <td>{row['Equipment Name']}</td>
                <td>
                  <span className="type-badge">{row.Type}</span>
                </td>
                <td>{row.Flowrate.toFixed(2)}</td>
                <td>{row.Pressure.toFixed(2)}</td>
                <td>{row.Temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DataTable;
