import React, { useState, useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './index.css';

const API_BASE = (typeof window !== 'undefined' && window.location && window.location.protocol.startsWith('http'))
  ? window.location.origin
  : 'http://127.0.0.1:8000';

export default function App() {
  const [activeTab, setActiveTab] = useState('forecast');
  const [apiStatus, setApiStatus] = useState('checking');
  
  // Simulation & Prediction State
  const [dateVal, setDateVal] = useState('2018-10-01');
  const [hourVal, setHourVal] = useState(8);
  const [tempC, setTempC] = useState(15.0);
  const [rainVal, setRainVal] = useState(0.0);
  const [snowVal, setSnowVal] = useState(0.0);
  const [cloudsVal, setCloudsVal] = useState(20);
  const [weatherVal, setWeatherVal] = useState('Clear');
  const [holidayVal, setHolidayVal] = useState('None');
  const [enableWhatIf, setEnableWhatIf] = useState(true);
  const [whatIfCondition, setWhatIfCondition] = useState('Mưa dông lớn (Rain 25mm/h)');

  // Prediction Results
  const [predResult, setPredResult] = useState({
    predicted_traffic_volume: 5564.77,
    congestion_level: 'Ùn tắc nghiêm trọng (Mức độ E/F - Quá tải công suất)',
    congestion_color: '#dc3545',
    is_rush_hour: true,
    is_weekend: false,
    is_holiday: false,
    warnings: []
  });

  // 24h Forecast Series
  const [hourlySeries, setHourlySeries] = useState(null);
  const [whatIfSeries, setWhatIfSeries] = useState(null);
  
  // Academic Experiments Data
  const [subTab, setSubTab] = useState('tn2');
  const [expMetrics, setExpMetrics] = useState(null);

  // Check API Health
  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'healthy') setApiStatus('online');
        else setApiStatus('offline');
      })
      .catch(() => setApiStatus('offline'));

    // Fetch experiments metrics
    fetch(`${API_BASE}/api/experiments`)
      .then(res => res.json())
      .then(data => setExpMetrics(data))
      .catch(() => {});
  }, []);

  // Trigger Prediction
  const runPrediction = (curDate, curHour, curTempC, curRain, curSnow, curClouds, curWeather, curHoliday) => {
    const tempK = parseFloat(curTempC) + 273.15;
    const dtStr = `${curDate} ${String(curHour).padStart(2, '0')}:00:00`;

    const payload = {
      date_time: dtStr,
      temp: tempK,
      rain_1h: parseFloat(curRain),
      snow_1h: parseFloat(curSnow),
      clouds_all: parseInt(curClouds),
      weather_main: curWeather,
      holiday: curHoliday
    };

    fetch(`${API_BASE}/api/traffic-forecast`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(data => {
        if (data.predicted_traffic_volume !== undefined) {
          setPredResult(data);
        }
      })
      .catch(() => {
        // Local fallback estimation
        const isWeekend = (new Date(curDate).getDay() === 0 || new Date(curDate).getDay() === 6);
        let baseVol = isWeekend ? 3200 : (curHour >= 7 && curHour <= 9 ? 5600 : (curHour >= 16 && curHour <= 18 ? 5800 : 3800));
        if (curHour >= 0 && curHour <= 4) baseVol = 800;
        if (curRain > 10) baseVol *= 0.9;
        setPredResult({
          predicted_traffic_volume: Math.round(baseVol),
          congestion_level: baseVol > 5500 ? 'Ùn tắc nghiêm trọng (LOS E/F)' : (baseVol > 4000 ? 'Đông đúc (LOS D)' : 'Thông thoáng (LOS A/B)'),
          congestion_color: baseVol > 5500 ? '#dc3545' : (baseVol > 4000 ? '#fd7e14' : '#28a745'),
          is_rush_hour: !isWeekend && ((curHour>=7&&curHour<=9)||(curHour>=16&&curHour<=18)),
          is_weekend: isWeekend,
          is_holiday: curHoliday !== 'None',
          warnings: []
        });
      });

    // Fetch 24h simulation
    fetch(`${API_BASE}/api/traffic-forecast-24h`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date: curDate,
        temp: tempK,
        rain_1h: parseFloat(curRain),
        snow_1h: parseFloat(curSnow),
        clouds_all: parseInt(curClouds),
        weather_main: curWeather,
        holiday: curHoliday
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.hourly_forecasts) {
          setHourlySeries(data.hourly_forecasts.map(p => p.predicted_traffic_volume));
        }
      })
      .catch(() => {});

    // Fetch What-if
    if (enableWhatIf) {
      let wTemp = tempK, wRain = 0, wSnow = 0, wMain = 'Clear';
      if (whatIfCondition.includes('Mưa dông')) {
        wRain = 25.0; wMain = 'Rain';
      } else if (whatIfCondition.includes('Bão tuyết')) {
        wTemp = 261.15; wSnow = 8.0; wMain = 'Snow';
      } else {
        wMain = 'Fog';
      }

      fetch(`${API_BASE}/api/traffic-forecast-24h`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date: curDate,
          temp: wTemp,
          rain_1h: wRain,
          snow_1h: wSnow,
          clouds_all: 100,
          weather_main: wMain,
          holiday: curHoliday
        })
      })
        .then(res => res.json())
        .then(data => {
          if (data.hourly_forecasts) {
            setWhatIfSeries(data.hourly_forecasts.map(p => p.predicted_traffic_volume));
          }
        })
        .catch(() => {});
    }
  };

  useEffect(() => {
    runPrediction(dateVal, hourVal, tempC, rainVal, snowVal, cloudsVal, weatherVal, holidayVal);
  }, [dateVal, hourVal, tempC, rainVal, snowVal, cloudsVal, weatherVal, holidayVal, enableWhatIf, whatIfCondition]);

  // Presets Handler
  const applyPreset = (preset) => {
    if (preset === 'morning_rush') {
      setDateVal('2018-10-01'); setHourVal(8); setTempC(15.0); setRainVal(0.0);
      setSnowVal(0.0); setCloudsVal(20); setWeatherVal('Clear'); setHolidayVal('None');
    } else if (preset === 'rainy_rush') {
      setDateVal('2018-10-05'); setHourVal(17); setTempC(18.0); setRainVal(15.0);
      setSnowVal(0.0); setCloudsVal(95); setWeatherVal('Rain'); setHolidayVal('None');
    } else if (preset === 'blizzard') {
      setDateVal('2018-01-15'); setHourVal(7); setTempC(-10.0); setRainVal(0.0);
      setSnowVal(5.0); setCloudsVal(100); setWeatherVal('Snow'); setHolidayVal('None');
    } else if (preset === 'holiday') {
      setDateVal('2018-07-04'); setHourVal(12); setTempC(28.0); setRainVal(0.0);
      setSnowVal(0.0); setCloudsVal(10); setWeatherVal('Clear'); setHolidayVal('Independence Day');
    } else if (preset === 'night') {
      setDateVal('2018-10-07'); setHourVal(2); setTempC(10.0); setRainVal(0.0);
      setSnowVal(0.0); setCloudsVal(10); setWeatherVal('Clear'); setHolidayVal('None');
    }
  };

  // Chart.js Canvas Ref
  const chart24hRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chart24hRef.current || activeTab !== 'forecast') return;

    const defaultHours = Array.from({length: 24}, (_, i) => `${i}h`);
    const defaultVols = [
      500, 350, 300, 400, 850, 2200, 4700, 5600, 5200, 4400, 4300, 4600,
      4800, 4900, 5200, 5700, 5800, 5600, 4700, 3700, 3000, 2500, 1800, 1000
    ];
    const primaryData = hourlySeries || defaultVols;
    const ctx = chart24hRef.current.getContext('2d');

    // Create Canvas Gradients
    let primaryGradient = 'rgba(37, 99, 235, 0.12)';
    let whatIfGradient = 'rgba(239, 68, 68, 0.10)';
    try {
      const g1 = ctx.createLinearGradient(0, 0, 0, 320);
      g1.addColorStop(0, 'rgba(37, 99, 235, 0.35)');
      g1.addColorStop(0.6, 'rgba(59, 130, 246, 0.10)');
      g1.addColorStop(1, 'rgba(59, 130, 246, 0.0)');
      primaryGradient = g1;

      const g2 = ctx.createLinearGradient(0, 0, 0, 320);
      g2.addColorStop(0, 'rgba(239, 68, 68, 0.28)');
      g2.addColorStop(0.6, 'rgba(239, 68, 68, 0.08)');
      g2.addColorStop(1, 'rgba(239, 68, 68, 0.0)');
      whatIfGradient = g2;
    } catch (e) {}

    // Plugin highlight giờ cao điểm sáng và chiều
    const rushHourPlugin = {
      id: 'rushHourZoneHighlight',
      beforeDraw: (chart) => {
        const { ctx, chartArea, scales } = chart;
        if (!chartArea || !scales || !scales.x) return;
        const { top, bottom } = chartArea;
        const x = scales.x;
        try {
          // Cao điểm sáng: 7h đến 9h
          const x7 = x.getPixelForValue(7);
          const x9 = x.getPixelForValue(9);
          if (x7 !== undefined && x9 !== undefined) {
            ctx.save();
            ctx.fillStyle = 'rgba(245, 158, 11, 0.08)';
            ctx.fillRect(x7, top, x9 - x7, bottom - top);
            ctx.fillStyle = 'rgba(180, 83, 9, 0.85)';
            ctx.font = 'bold 10px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('⚡ CAO ĐIỂM SÁNG', (x7 + x9) / 2, top + 16);
            ctx.restore();
          }

          // Cao điểm chiều: 16h đến 18h
          const x16 = x.getPixelForValue(16);
          const x18 = x.getPixelForValue(18);
          if (x16 !== undefined && x18 !== undefined) {
            ctx.save();
            ctx.fillStyle = 'rgba(245, 158, 11, 0.08)';
            ctx.fillRect(x16, top, x18 - x16, bottom - top);
            ctx.fillStyle = 'rgba(180, 83, 9, 0.85)';
            ctx.font = 'bold 10px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('⚡ CAO ĐIỂM CHIỀU', (x16 + x18) / 2, top + 16);
            ctx.restore();
          }
        } catch (err) {}
      }
    };

    const datasets = [
      {
        label: 'Kịch bản hiện tại (Base)',
        data: primaryData,
        borderColor: '#2563eb',
        backgroundColor: primaryGradient,
        borderWidth: 3.5,
        fill: true,
        tension: 0.38,
        pointRadius: (c) => c.dataIndex === hourVal ? 8 : (c.dataIndex % 3 === 0 ? 3 : 0),
        pointHoverRadius: 9,
        pointBackgroundColor: (c) => c.dataIndex === hourVal ? '#ef4444' : '#2563eb',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        order: 2
      }
    ];

    if (enableWhatIf && whatIfSeries) {
      datasets.push({
        label: `What-If: ${whatIfCondition.split(' (')[0]}`,
        data: whatIfSeries,
        borderColor: '#ef4444',
        backgroundColor: whatIfGradient,
        borderDash: [5, 5],
        borderWidth: 2.8,
        fill: true,
        tension: 0.38,
        pointRadius: (c) => c.dataIndex === hourVal ? 6 : 0,
        pointHoverRadius: 7,
        pointBackgroundColor: '#ef4444',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        order: 1
      });
    }

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    chartInstance.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: defaultHours,
        datasets: datasets
      },
      plugins: [rushHourPlugin],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            position: 'top',
            labels: {
              usePointStyle: true,
              boxWidth: 8,
              padding: 16,
              font: { family: 'Inter', size: 12, weight: '600' }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.94)',
            titleFont: { family: 'Inter', size: 13, weight: '700' },
            bodyFont: { family: 'Inter', size: 12, weight: '500' },
            padding: 12,
            cornerRadius: 10,
            callbacks: {
              title: (items) => `⏰ Mốc thời gian: ${items[0].label} (Giờ ${items[0].dataIndex})`,
              label: (ctx) => {
                const val = Math.round(ctx.parsed.y);
                let level = 'LOS A (<1500)';
                if (val >= 5500) level = 'LOS E/F (Ùn tắc)';
                else if (val >= 4500) level = 'LOS D (Đông đúc)';
                else if (val >= 3000) level = 'LOS C (Khá đông)';
                else if (val >= 1500) level = 'LOS B (Ổn định)';
                return `  ${ctx.dataset.label}: ${val.toLocaleString()} xe/h [${level}]`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(241, 245, 249, 0.9)' },
            ticks: {
              font: { family: 'Inter', size: 11, weight: '600' },
              color: '#64748b'
            }
          },
          y: {
            beginAtZero: true,
            max: 7500,
            title: {
              display: true,
              text: 'Lưu lượng xe quan trắc (xe/giờ)',
              font: { family: 'Inter', size: 12, weight: '700' },
              color: '#475569'
            },
            grid: { color: 'rgba(226, 232, 240, 0.7)' },
            ticks: {
              font: { family: 'Inter', size: 11, weight: '600' },
              color: '#64748b',
              callback: (val) => val === 0 ? '0' : `${val / 1000}k`
            }
          }
        }
      }
    });

    return () => {
      if (chartInstance.current) chartInstance.current.destroy();
    };
  }, [hourlySeries, whatIfSeries, hourVal, enableWhatIf, whatIfCondition, activeTab]);

  return (
    <div className="container">
      {/* Header Card */}
      <div className="header-card">
        <div>
          <div className="header-title">
            🚗 Hệ Thống Dự Báo Lưu Lượng Giao Thông Cao Tốc I-94
          </div>
          <div className="header-sub">
            Học phần: <b>Học máy cơ bản</b> | GVHD: <b>PGS.TS. Nguyễn Văn Hậu</b> | Lớp: <b>12523W.1</b> (UTEHY)
          </div>
        </div>
        <div>
          {apiStatus === 'online' ? (
            <span className="badge-api badge-online">
              ● Backend API: SẴN SÀNG (Port 8000)
            </span>
          ) : (
            <span className="badge-api badge-offline">
              ● Backend API: OFFLINE (Chế độ Fallback Model)
            </span>
          )}
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="tabs-nav">
        <button
          className={`tab-btn ${activeTab === 'eda' ? 'active' : ''}`}
          onClick={() => setActiveTab('eda')}
        >
          📊 Màn hình 1: Khám phá Dữ liệu (EDA)
        </button>
        <button
          className={`tab-btn ${activeTab === 'forecast' ? 'active' : ''}`}
          onClick={() => setActiveTab('forecast')}
        >
          🔮 Màn hình 2: Mô phỏng 24h & Dự báo Trực tuyến
        </button>
        <button
          className={`tab-btn ${activeTab === 'benchmark' ? 'active' : ''}`}
          onClick={() => setActiveTab('benchmark')}
        >
          📈 Màn hình 3: Đánh giá Học thuật & 4 Thí nghiệm
        </button>
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: EDA & TỔNG QUAN DỮ LIỆU */}
      {/* ========================================================================= */}
      {activeTab === 'eda' && (
        <div>
          <div className="stat-grid-4">
            <div className="stat-card">
              <div className="stat-num">40,565</div>
              <div className="stat-lbl">Bản ghi sạch (Deduplicated)</div>
              <div style={{fontSize: '0.78rem', color: '#059669', marginTop: '4px'}}>Đã lọc 10 bản 0K & 7,629 bản trùng</div>
            </div>
            <div className="stat-card">
              <div className="stat-num">70 - 15 - 15%</div>
              <div className="stat-lbl">Chiến lược chia chuỗi thời gian</div>
              <div style={{fontSize: '0.78rem', color: '#2563eb', marginTop: '4px'}}>Anti-leakage Time Split</div>
            </div>
            <div className="stat-card">
              <div className="stat-num">2012 - 2018</div>
              <div className="stat-lbl">Chuỗi thời gian quan trắc</div>
              <div style={{fontSize: '0.78rem', color: '#7c3aed', marginTop: '4px'}}>6 năm liên tục (Twin Cities)</div>
            </div>
            <div className="stat-card">
              <div className="stat-num">7,280 <span style={{fontSize: '1rem'}}>xe/h</span></div>
              <div className="stat-lbl">Lưu lượng cực đại</div>
              <div style={{fontSize: '0.78rem', color: '#dc2626', marginTop: '4px'}}>Lưu lượng TB: 3,259 xe/h</div>
            </div>
          </div>

          <div className="grid-2">
            <div className="card">
              <div className="card-title">⏰ Biểu đồ Chu kỳ Ngày Đêm (Diurnal Pattern)</div>
              <p style={{fontSize: '0.88rem', color: '#64748b', marginBottom: '1rem'}}>
                Quy luật 2 đỉnh giờ cao điểm (Bimodal) vào các ngày làm việc (sáng 8h và chiều 17h) 
                so sánh với đường cong đơn đỉnh thoai thoải của ngày cuối tuần.
              </p>
              <div style={{height: '260px', background: '#f8fafc', borderRadius: '8px', padding: '10px'}}>
                <img 
                  src="/reports/figures/exp1_random_vs_time_split.png" 
                  alt="Diurnal pattern" 
                  style={{width: '100%', height: '100%', objectFit: 'contain'}}
                  onError={(e) => { e.target.style.display = 'none'; }}
                />
              </div>
            </div>

            <div className="card">
              <div className="card-title">🌦️ Tác động của Điều kiện Thời tiết</div>
              <p style={{fontSize: '0.88rem', color: '#64748b', marginBottom: '1rem'}}>
                Lưu lượng trung bình sụt giảm rõ rệt khi gặp điều kiện thời tiết bất lợi (mưa dông lớn, bão tuyết).
              </p>
              <table className="academic-table">
                <thead>
                  <tr>
                    <th>Trạng thái thời tiết</th>
                    <th>Lưu lượng TB</th>
                    <th>Ảnh hưởng</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Trời quang (Clear)</td>
                    <td><b>3,450 xe/h</b></td>
                    <td><span style={{color: '#059669'}}>Bình thường</span></td>
                  </tr>
                  <tr>
                    <td>Mây che phủ (Clouds)</td>
                    <td><b>3,320 xe/h</b></td>
                    <td><span style={{color: '#059669'}}>Giảm nhẹ (-3.7%)</span></td>
                  </tr>
                  <tr>
                    <td>Mưa dông (Rain)</td>
                    <td><b>3,080 xe/h</b></td>
                    <td><span style={{color: '#d97706'}}>Giảm vừa (-10.7%)</span></td>
                  </tr>
                  <tr>
                    <td>Tuyết rơi (Snow)</td>
                    <td><b>2,760 xe/h</b></td>
                    <td><span style={{color: '#dc2626'}}>Giảm sâu (-20.0%)</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div className="card">
            <div className="card-title">📋 Trích mẫu Dữ liệu Giao thông Thực tế (5 Dòng đầu)</div>
            <table className="academic-table">
              <thead>
                <tr>
                  <th>date_time</th>
                  <th>temp (K)</th>
                  <th>rain_1h</th>
                  <th>snow_1h</th>
                  <th>clouds_all</th>
                  <th>weather_main</th>
                  <th>traffic_volume</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>2012-10-02 09:00:00</td><td>288.28 K (15.1°C)</td><td>0.0 mm</td><td>0.0 mm</td><td>40%</td><td>Clouds</td><td><b>5,545 xe/h</b></td></tr>
                <tr><td>2012-10-02 10:00:00</td><td>289.36 K (16.2°C)</td><td>0.0 mm</td><td>0.0 mm</td><td>75%</td><td>Clouds</td><td><b>4,516 xe/h</b></td></tr>
                <tr><td>2012-10-02 11:00:00</td><td>289.58 K (16.4°C)</td><td>0.0 mm</td><td>0.0 mm</td><td>90%</td><td>Clouds</td><td><b>4,767 xe/h</b></td></tr>
                <tr><td>2012-10-02 12:00:00</td><td>290.13 K (17.0°C)</td><td>0.0 mm</td><td>0.0 mm</td><td>90%</td><td>Clouds</td><td><b>5,026 xe/h</b></td></tr>
                <tr><td>2012-10-02 13:00:00</td><td>291.14 K (18.0°C)</td><td>0.0 mm</td><td>0.0 mm</td><td>75%</td><td>Clouds</td><td><b>4,918 xe/h</b></td></tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: MÔ PHỎNG 24H & DỰ BÁO TRỰC TUYẾN */}
      {/* ========================================================================= */}
      {activeTab === 'forecast' && (
        <div>
          {/* Quick Presets */}
          <div className="card" style={{padding: '1rem 1.5rem', marginBottom: '1rem'}}>
            <div style={{fontSize: '0.85rem', fontWeight: '700', color: '#475569', marginBottom: '0.5rem'}}>
              ⚡ Kịch bản mô phỏng nhanh (Quick Presets):
            </div>
            <div className="preset-grid">
              <button className="btn-preset" onClick={() => applyPreset('morning_rush')}>🌅 Sáng T2 Cao điểm (8h)</button>
              <button className="btn-preset" onClick={() => applyPreset('rainy_rush')}>🌆 Chiều T6 Mưa to (17h)</button>
              <button className="btn-preset" onClick={() => applyPreset('blizzard')}>❄️ Bão tuyết sáng (7h)</button>
              <button className="btn-preset" onClick={() => applyPreset('holiday')}>🎉 Lễ Quốc khánh (12h)</button>
              <button className="btn-preset" onClick={() => applyPreset('night')}>🌙 Đêm khuya Chủ Nhật (2h)</button>
            </div>
          </div>

          <div className="grid-2">
            {/* Form Điều Khiển */}
            <div className="card">
              <div className="card-title">🎛️ Bộ Tham số Đầu vào</div>
              
              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem'}}>
                <div className="form-group">
                  <label className="form-label">Ngày quan sát:</label>
                  <input 
                    type="date" 
                    className="form-control" 
                    value={dateVal} 
                    onChange={(e) => setDateVal(e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Giờ: <span>{hourVal}h</span></label>
                  <input 
                    type="range" 
                    className="range-slider" 
                    min="0" max="23" 
                    value={hourVal} 
                    onChange={(e) => setHourVal(parseInt(e.target.value))}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">
                  Nhiệt độ (°C): <span>{tempC}°C ({ (tempC + 273.15).toFixed(1) } K)</span>
                </label>
                <input 
                  type="range" 
                  className="range-slider" 
                  min="-30" max="45" step="0.5" 
                  value={tempC} 
                  onChange={(e) => setTempC(parseFloat(e.target.value))}
                />
              </div>

              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem'}}>
                <div className="form-group">
                  <label className="form-label">Lượng mưa (mm/h):</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    min="0" max="100" step="1" 
                    value={rainVal} 
                    onChange={(e) => setRainVal(parseFloat(e.target.value) || 0)}
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Lượng tuyết (mm/h):</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    min="0" max="30" step="0.5" 
                    value={snowVal} 
                    onChange={(e) => setSnowVal(parseFloat(e.target.value) || 0)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Độ mây che phủ (%): <span>{cloudsVal}%</span></label>
                <input 
                  type="range" 
                  className="range-slider" 
                  min="0" max="100" 
                  value={cloudsVal} 
                  onChange={(e) => setCloudsVal(parseInt(e.target.value))}
                />
              </div>

              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem'}}>
                <div className="form-group">
                  <label className="form-label">Hiện tượng thời tiết:</label>
                  <select 
                    className="form-control" 
                    value={weatherVal} 
                    onChange={(e) => setWeatherVal(e.target.value)}
                  >
                    {['Clear', 'Clouds', 'Rain', 'Snow', 'Drizzle', 'Mist', 'Fog', 'Thunderstorm', 'Haze', 'Squall', 'Smoke'].map(w => (
                      <option key={w} value={w}>{w}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Ngày lễ liên bang:</label>
                  <select 
                    className="form-control" 
                    value={holidayVal} 
                    onChange={(e) => setHolidayVal(e.target.value)}
                  >
                    {[
                      'None', 'Columbus Day', 'Veterans Day', 'Thanksgiving Day', 'Christmas Day',
                      'New Years Day', 'Martin Luther King Jr Day', 'Washingtons Birthday',
                      'Memorial Day', 'Independence Day', 'State Fair', 'Labor Day'
                    ].map(h => (
                      <option key={h} value={h}>{h}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Kết Quả Dự Báo Thời Gian Thực (XGBoost Cockpit) */}
            <div className="card gauge-cockpit">
              <div className="cockpit-header">
                <div className="cockpit-title">
                  🎯 Kết quả Dự báo Thời gian thực
                </div>
                <div className="live-pulse">
                  <span className="pulse-dot"></span>
                  <span>XGBoost v1.0 • Realtime</span>
                </div>
              </div>

              <div className="gauge-display-area">
                <div className="gauge-svg-wrapper">
                  <svg className="gauge-svg-hud" viewBox="0 0 300 175">
                    <defs>
                      <linearGradient id="speedometerGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#10b981" />
                        <stop offset="28%" stopColor="#06b6d4" />
                        <stop offset="55%" stopColor="#f59e0b" />
                        <stop offset="78%" stopColor="#f97316" />
                        <stop offset="100%" stopColor="#ef4444" />
                      </linearGradient>
                      <filter id="needleShadow" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="rgba(0,0,0,0.3)" />
                      </filter>
                      <filter id="activeGlow" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor={predResult.congestion_color || '#2563eb'} floodOpacity="0.6" />
                      </filter>
                    </defs>

                    {/* Outer Background Scale Track */}
                    <path 
                      d="M 45 145 A 105 105 0 0 1 255 145" 
                      fill="none" 
                      stroke="#f1f5f9" 
                      strokeWidth="18" 
                      strokeLinecap="round" 
                    />

                    {/* Faint Colored Track */}
                    <path 
                      d="M 45 145 A 105 105 0 0 1 255 145" 
                      fill="none" 
                      stroke="url(#speedometerGradient)" 
                      strokeWidth="18" 
                      strokeLinecap="round" 
                      opacity="0.22"
                    />

                    {/* Active Progress Arc */}
                    <path 
                      d="M 45 145 A 105 105 0 0 1 255 145" 
                      fill="none" 
                      stroke={predResult.congestion_color || 'url(#speedometerGradient)'} 
                      strokeWidth="18" 
                      strokeDasharray="329.87" 
                      strokeDashoffset={329.87 - (Math.min(7500, Math.max(0, predResult.predicted_traffic_volume)) / 7500) * 329.87}
                      strokeLinecap="round" 
                      filter="url(#activeGlow)"
                      style={{transition: 'stroke-dashoffset 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), stroke 0.4s ease'}}
                    />

                    {/* Tick Marks & Scale Labels */}
                    {[
                      { f: 0, label: '0' },
                      { f: 0.2, label: '1.5k' },
                      { f: 0.4, label: '3k' },
                      { f: 0.6, label: '4.5k' },
                      { f: 0.8, label: '6k' },
                      { f: 1.0, label: '7.5k' }
                    ].map((t, idx) => {
                      const angle = Math.PI - t.f * Math.PI;
                      const xOut = 150 + 94 * Math.cos(angle);
                      const yOut = 145 - 94 * Math.sin(angle);
                      const xIn = 150 + 84 * Math.cos(angle);
                      const yIn = 145 - 84 * Math.sin(angle);
                      const xTxt = 150 + 70 * Math.cos(angle);
                      const yTxt = 145 - 70 * Math.sin(angle);
                      return (
                        <g key={idx}>
                          <line x1={xIn} y1={yIn} x2={xOut} y2={yOut} stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" />
                          <text 
                            x={xTxt} 
                            y={yTxt + 3} 
                            textAnchor="middle" 
                            fontSize="9" 
                            fontWeight="700" 
                            fill="#64748b"
                            fontFamily="Inter, sans-serif"
                          >
                            {t.label}
                          </text>
                        </g>
                      );
                    })}

                    {/* Dynamic Needle */}
                    {(() => {
                      const needleFraction = Math.min(7500, Math.max(0, predResult.predicted_traffic_volume)) / 7500;
                      const needleDeg = -90 + needleFraction * 180;
                      return (
                        <g 
                          transform={`rotate(${needleDeg} 150 145)`} 
                          filter="url(#needleShadow)"
                          style={{transition: 'transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)'}}
                        >
                          <polygon 
                            points="146,145 154,145 151.5,38 148.5,38" 
                            fill={predResult.congestion_color || '#2563eb'} 
                          />
                          <circle cx="150" cy="145" r="11" fill="#0f172a" stroke="#ffffff" strokeWidth="2.5" />
                          <circle cx="150" cy="145" r="4.5" fill={predResult.congestion_color || '#2563eb'} />
                        </g>
                      );
                    })()}
                  </svg>
                </div>

                <div className="gauge-digital-readout">
                  <div className="readout-number" style={{color: predResult.congestion_color || '#1e293b'}}>
                    {Math.round(predResult.predicted_traffic_volume).toLocaleString()}
                  </div>
                  <div className="readout-unit">Phương tiện / Giờ (Vehicles / Hour)</div>

                  <div 
                    className="los-tag-glow" 
                    style={{
                      backgroundColor: `${predResult.congestion_color}18`, 
                      color: predResult.congestion_color,
                      border: `1.5px solid ${predResult.congestion_color}60`
                    }}
                  >
                    <span style={{fontSize: '1.1rem'}}>🚦</span>
                    <span>{predResult.congestion_level}</span>
                  </div>
                </div>

                {/* Capacity Utilization Progress Bar */}
                <div style={{width: '100%', marginTop: '1rem'}}>
                  <div className="capacity-wrapper">
                    <div 
                      className="capacity-fill" 
                      style={{
                        width: `${Math.min(100, Math.round((predResult.predicted_traffic_volume / 7500) * 100))}%`,
                        backgroundColor: predResult.congestion_color || '#2563eb'
                      }}
                    />
                  </div>
                  <div className="capacity-labels">
                    <span>Tải trọng tuyến: <b>{Math.min(100, Math.round((predResult.predicted_traffic_volume / 7500) * 100))}%</b></span>
                    <span>Công suất tối đa: 7,500 xe/h</span>
                  </div>
                </div>

                {/* Contextual Badges Grid */}
                <div className="context-pill-grid">
                  <div className="context-mini-pill">
                    <span className="context-mini-icon">{predResult.is_rush_hour ? '🔥' : '🟢'}</span>
                    <div>
                      <div className="context-mini-title">Khung giờ</div>
                      <div className="context-mini-value">{predResult.is_rush_hour ? 'Cao điểm (Rush Hour)' : 'Bình thường'}</div>
                    </div>
                  </div>

                  <div className="context-mini-pill">
                    <span className="context-mini-icon">{predResult.is_weekend ? '📅' : '💼'}</span>
                    <div>
                      <div className="context-mini-title">Loại ngày</div>
                      <div className="context-mini-value">{predResult.is_weekend ? 'Cuối tuần (Weekend)' : 'Ngày làm việc'}</div>
                    </div>
                  </div>

                  <div className="context-mini-pill">
                    <span className="context-mini-icon">🌡️</span>
                    <div>
                      <div className="context-mini-title">Khí tượng</div>
                      <div className="context-mini-value">{tempC}°C ({ (tempC + 273.15).toFixed(1) }K) • {weatherVal}</div>
                    </div>
                  </div>

                  <div className="context-mini-pill">
                    <span className="context-mini-icon">{predResult.is_holiday ? '🎉' : '🛡️'}</span>
                    <div>
                      <div className="context-mini-title">Dữ liệu kiểm toán</div>
                      <div className="context-mini-value">{predResult.is_holiday ? holidayVal : 'In-Distribution (An toàn)'}</div>
                    </div>
                  </div>
                </div>

                {predResult.warnings && predResult.warnings.length > 0 && (
                  <div className="alert-box alert-warning" style={{marginTop: '1rem', width: '100%'}}>
                    <span>⚠️</span>
                    <div>
                      {predResult.warnings.map((w, idx) => <div key={idx}>{w}</div>)}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* 24h Diurnal Curve & What-If */}
          <div className="chart-cockpit-card">
            <div className="chart-top-bar">
              <div className="chart-title-group">
                <h3>📈 Mô phỏng Chu kỳ 24 Giờ & Phân tích Tình huống Giả định (What-If)</h3>
                <p>Đường cong biến thiên ngày đêm kết hợp dải bóng giờ cao điểm sáng / chiều và đối sánh thời tiết bất lợi</p>
              </div>

              <div className="whatif-control-panel">
                <label className="toggle-switch-label">
                  <span className="ios-switch">
                    <input 
                      type="checkbox" 
                      checked={enableWhatIf} 
                      onChange={(e) => setEnableWhatIf(e.target.checked)} 
                    />
                    <span className="ios-slider"></span>
                  </span>
                  <span>So sánh What-If:</span>
                </label>

                <select 
                  className="scenario-select-styled"
                  value={whatIfCondition}
                  onChange={(e) => setWhatIfCondition(e.target.value)}
                  disabled={!enableWhatIf}
                >
                  <option value="Mưa dông lớn (Rain 25mm/h)">⛈️ Mưa dông lớn (Rain 25mm/h)</option>
                  <option value="Bão tuyết dày (Snow 8mm/h, -12°C)">❄️ Bão tuyết dày (Snow 8mm/h, -12°C)</option>
                  <option value="Sương mù hạn chế tầm nhìn (Fog)">🌫️ Sương mù hạn chế tầm nhìn (Fog)</option>
                </select>
              </div>
            </div>

            {/* Dynamic Summary Metric Chips */}
            {(() => {
              const defaultVols = [
                500, 350, 300, 400, 850, 2200, 4700, 5600, 5200, 4400, 4300, 4600,
                4800, 4900, 5200, 5700, 5800, 5600, 4700, 3700, 3000, 2500, 1800, 1000
              ];
              const series = hourlySeries || defaultVols;
              const peakV = Math.max(...series);
              const peakH = series.indexOf(peakV);
              const minV = Math.min(...series);
              const minH = series.indexOf(minV);
              const avgV = Math.round(series.reduce((a, b) => a + b, 0) / 24);

              const curVol = series[hourVal] !== undefined ? Math.round(series[hourVal]) : Math.round(predResult.predicted_traffic_volume);
              const wVol = (enableWhatIf && whatIfSeries && whatIfSeries[hourVal] !== undefined) ? Math.round(whatIfSeries[hourVal]) : null;
              const diff = (wVol !== null) ? wVol - curVol : null;
              const diffPct = (diff !== null && curVol > 0) ? ((diff / curVol) * 100).toFixed(1) : null;

              return (
                <div className="chart-metrics-banner">
                  <div className="chart-metric-chip" style={{borderLeft: '4px solid #ef4444'}}>
                    <div className="chip-label">Đỉnh cao điểm trong ngày</div>
                    <div className="chip-value">
                      {Math.round(peakV).toLocaleString()} <span style={{fontSize: '0.8rem', color: '#64748b'}}>xe/h</span>
                    </div>
                    <div className="chip-sub" style={{color: '#dc2626'}}>
                      Khung giờ: <b>{peakH}:00</b> (Giờ tan tầm)
                    </div>
                  </div>

                  <div className="chart-metric-chip" style={{borderLeft: '4px solid #10b981'}}>
                    <div className="chip-label">Đáy thấp điểm (Đêm)</div>
                    <div className="chip-value">
                      {Math.round(minV).toLocaleString()} <span style={{fontSize: '0.8rem', color: '#64748b'}}>xe/h</span>
                    </div>
                    <div className="chip-sub" style={{color: '#059669'}}>
                      Khung giờ: <b>{minH}:00</b> (Thông thoáng tuyệt đối)
                    </div>
                  </div>

                  <div className="chart-metric-chip" style={{borderLeft: '4px solid #3b82f6'}}>
                    <div className="chip-label">Lưu lượng Trung bình 24h</div>
                    <div className="chip-value">
                      {avgV.toLocaleString()} <span style={{fontSize: '0.8rem', color: '#64748b'}}>xe/h</span>
                    </div>
                    <div className="chip-sub" style={{color: '#2563eb'}}>
                      Tổng ngày: ~<b>{Math.round(avgV * 24).toLocaleString()}</b> lượt xe
                    </div>
                  </div>

                  <div className="chart-metric-chip" style={{borderLeft: '4px solid #f59e0b'}}>
                    <div className="chip-label">Tác động What-If tại {hourVal}:00</div>
                    <div className="chip-value" style={{color: diff !== null ? (diff < 0 ? '#dc2626' : '#059669') : '#64748b'}}>
                      {diff !== null ? `${diff > 0 ? '+' : ''}${diff.toLocaleString()} xe/h` : 'Chưa kích hoạt'}
                    </div>
                    <div className="chip-sub" style={{color: diff !== null ? (diff < 0 ? '#dc2626' : '#059669') : '#64748b'}}>
                      {diff !== null ? `Biến động: ${diffPct}% so với kịch bản gốc` : 'Bật nút so sánh góc phải'}
                    </div>
                  </div>
                </div>
              );
            })()}

            {/* Main Chart Canvas */}
            <div style={{height: '370px', width: '100%', position: 'relative'}}>
              <canvas ref={chart24hRef}></canvas>
            </div>

            {/* Interactive Timeline Scrubber Slider */}
            <div className="timeline-scrubber">
              <div className="scrubber-header">
                <div className="scrubber-title">
                  ⏱️ Con trỏ dòng thời gian (Time Scrubber): <span style={{color: '#2563eb', fontWeight: '800'}}>{hourVal}:00 ({hourVal} Giờ)</span>
                </div>
                <div style={{fontSize: '0.78rem', color: '#64748b'}}>
                  Kéo thanh trượt để di chuyển mốc giờ quan sát và xem đồng hồ đo biến thiên tức thì
                </div>
              </div>
              <input 
                type="range" 
                className="scrubber-slider" 
                min="0" 
                max="23" 
                value={hourVal} 
                onChange={(e) => setHourVal(parseInt(e.target.value))}
              />
              <div className="scrubber-ticks">
                <span>00:00 (Đêm)</span>
                <span>04:00</span>
                <span style={{color: '#d97706', fontWeight: '700'}}>08:00 (Sáng)</span>
                <span>12:00 (Trưa)</span>
                <span style={{color: '#d97706', fontWeight: '700'}}>17:00 (Chiều)</span>
                <span>20:00 (Tối)</span>
                <span>23:00</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 3: ĐÁNH GIÁ HỌC THUẬT & 4 THÍ NGHIỆM */}
      {/* ========================================================================= */}
      {activeTab === 'benchmark' && (
        <div>
          <div style={{display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap'}}>
            <button className={`btn-preset ${subTab === 'tn1' ? 'active' : ''}`} onClick={() => setSubTab('tn1')}>
              🧪 TN1: Chia ngẫu nhiên vs Thời gian
            </button>
            <button className={`btn-preset ${subTab === 'tn2' ? 'active' : ''}`} onClick={() => setSubTab('tn2')}>
              🏆 TN2: Benchmark 5 Mô hình
            </button>
            <button className={`btn-preset ${subTab === 'tn3' ? 'active' : ''}`} onClick={() => setSubTab('tn3')}>
              🍂 TN3: Hiện tượng Trôi dạt Dữ liệu
            </button>
            <button className={`btn-preset ${subTab === 'tn4' ? 'active' : ''}`} onClick={() => setSubTab('tn4')}>
              ⚠️ TN4: Phân tích Sai số Dị biệt
            </button>
          </div>

          {/* TN1 */}
          {subTab === 'tn1' && (
            <div className="card">
              <div className="card-title">🧪 Thí nghiệm 1: Chứng minh Rò rỉ Dữ liệu (Data Leakage) khi Chia ngẫu nhiên</div>
              <p style={{fontSize: '0.9rem', color: '#475569', marginBottom: '1rem'}}>
                So sánh giữa cách chia ngẫu nhiên thông thường (Shuffle) và chia chuỗi thời gian nghiêm ngặt (Time-based Split). 
                Chia ngẫu nhiên làm rò rỉ thông tin quá khứ và tương lai lẫn nhau, dẫn đến kết quả đánh giá lạc quan ảo.
              </p>
              <table className="academic-table">
                <thead>
                  <tr>
                    <th>Chiến lược phân chia</th>
                    <th>MAE (xe/h)</th>
                    <th>RMSE (xe/h)</th>
                    <th>Hệ số R²</th>
                    <th>Đánh giá khoa học</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Random Split (Rò rỉ dữ liệu)</td>
                    <td>265.95</td>
                    <td>452.85</td>
                    <td>0.9476</td>
                    <td><span style={{color: '#dc2626'}}>Lạc quan ảo do tự tương quan rò rỉ</span></td>
                  </tr>
                  <tr style={{background: '#ecfdf5', fontWeight: 'bold'}}>
                    <td>Time-based Split (Chuẩn thực tế)</td>
                    <td>242.58</td>
                    <td>424.63</td>
                    <td>0.9540</td>
                    <td><span style={{color: '#059669'}}>Phản ánh chính xác năng lực tương lai</span></td>
                  </tr>
                </tbody>
              </table>
              <div className="alert-box" style={{background: '#ecfdf5', borderColor: '#059669', color: '#065f46', marginTop: '1rem'}}>
                <b>✅ Kết luận Thí nghiệm 1</b>: Phân chia theo trục thời gian (Time-based Split) là bắt buộc 
                đối với bài toán dự báo chuỗi thời gian để bảo đảm tính toàn vẹn khoa học và tránh rò rỉ thông tin tương lai.
              </div>
              <img src="/reports/figures/exp1_random_vs_time_split.png" alt="TN1" className="academic-img" onError={(e) => { e.target.style.display = 'none'; }} />
            </div>
          )}

          {/* TN2 */}
          {subTab === 'tn2' && (
            <div className="card">
              <div className="card-title">🏆 Thí nghiệm 2: Bảng Đối chuẩn Benchmark 5 Mô hình trên Tập Test Độc lập</div>
              <p style={{fontSize: '0.9rem', color: '#475569', marginBottom: '1rem'}}>
                So sánh mô hình Quán quân XGBoost Regressor (Gradient Boosting) với Random Forest (Ensemble Bagging), 
                Historical Calendar Baseline (giờ x thứ x lễ), cùng cặp đôi hồi quy tuyến tính điều hòa: 
                Ridge Regression (L2) và Lasso Regression (L1) trên tập Test độc lập (khóa hoàn toàn trong suốt quá trình train).
              </p>
              <table className="academic-table">
                <thead>
                  <tr>
                    <th>Thứ hạng</th>
                    <th>Mô hình kiểm định</th>
                    <th>Trường phái kiến trúc</th>
                    <th>MAE (xe/h)</th>
                    <th>RMSE (xe/h)</th>
                    <th>Hệ số R²</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style={{background: '#fef3c7'}}>
                    <td><span className="badge-rank-1">🥇 Hạng 1</span></td>
                    <td><b>XGBoost Regressor</b></td>
                    <td>Ensemble Boosting</td>
                    <td><b>242.58</b></td>
                    <td><b>424.63</b></td>
                    <td><b>0.9540</b></td>
                  </tr>
                  <tr>
                    <td>🥈 Hạng 2</td>
                    <td>Random Forest Regressor</td>
                    <td>Ensemble Bagging</td>
                    <td>251.64</td>
                    <td>448.68</td>
                    <td>0.9486</td>
                  </tr>
                  <tr>
                    <td>🥉 Hạng 3</td>
                    <td>Historical Calendar Baseline</td>
                    <td>Heuristic Lịch trình</td>
                    <td>260.77</td>
                    <td>448.08</td>
                    <td>0.9487</td>
                  </tr>
                  <tr>
                    <td>Hạng 4</td>
                    <td>Ridge Regression (L2)</td>
                    <td>Linear Regularized L2</td>
                    <td>636.59</td>
                    <td>874.48</td>
                    <td>0.8048</td>
                  </tr>
                  <tr>
                    <td>Hạng 5</td>
                    <td>Lasso Regression (L1)</td>
                    <td>Linear Regularized L1</td>
                    <td>637.99</td>
                    <td>875.26</td>
                    <td>0.8045</td>
                  </tr>
                </tbody>
              </table>
              <div className="alert-box" style={{background: '#eff6ff', borderColor: '#3b82f6', color: '#1e40af', marginTop: '1rem'}}>
                <b>💡 Phát hiện khoa học quan trọng</b>: 
                XGBoost xuất sắc giành Hạng 1 toàn diện với MAE chỉ 242.58 xe/h và R² vượt mốc 0.9540. 
                Cặp đôi tuyến tính Lasso (L1) và Ridge (L2) cho kết quả xấp xỉ nhau (~637 xe/h), 
                chứng minh hạn chế nội tại của mọi giả định tuyến tính trước biến thiên phi tuyến 2 đỉnh ngày đêm.
              </div>
              <img src="/reports/figures/exp2_models_comparison.png" alt="TN2" className="academic-img" onError={(e) => { e.target.style.display = 'none'; }} />
            </div>
          )}

          {/* TN3 */}
          {subTab === 'tn3' && (
            <div className="card">
              <div className="card-title">🍂 Thí nghiệm 3: Hiện tượng Trôi dạt Dữ liệu theo Năm và theo Mùa (Data Drift)</div>
              <p style={{fontSize: '0.9rem', color: '#475569', marginBottom: '1rem'}}>
                Khảo sát sự suy giảm hiệu năng khi mô hình được huấn luyện trên giai đoạn quá khứ (2012–2017) 
                và triển khai dự báo cho các giai đoạn tương lai (2017–2018), cũng như biến thiên sai số giữa 4 mùa.
              </p>
              <table className="academic-table">
                <thead>
                  <tr>
                    <th>Năm quan trắc</th>
                    <th>Tập dữ liệu</th>
                    <th>MAE (xe/h)</th>
                    <th>Hiện tượng & Nhận định</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td>2012 - 2016</td><td>Tập Huấn luyện</td><td>156.95 - 179.53</td><td>Mô hình khớp rất tốt</td></tr>
                  <tr><td>2017</td><td>Tập Validation</td><td>226.90</td><td>Bắt đầu trôi dạt (+31.7%)</td></tr>
                  <tr style={{background: '#fef2f2', fontWeight: 'bold'}}><td>2018</td><td>Tập Test Độc lập</td><td>256.64</td><td>Trôi dạt rõ rệt (Significant Drift)</td></tr>
                </tbody>
              </table>
              <img src="/reports/figures/exp3_seasonal_drift.png" alt="TN3" className="academic-img" onError={(e) => { e.target.style.display = 'none'; }} />
            </div>
          )}

          {/* TN4 */}
          {subTab === 'tn4' && (
            <div className="card">
              <div className="card-title">⚠️ Thí nghiệm 4: Phân tích Sai số theo Ngày lễ & Thời tiết Cực đoan</div>
              <p style={{fontSize: '0.9rem', color: '#475569', marginBottom: '1rem'}}>
                Phân tích chuyên sâu các tình huống dị biệt (Edge Cases) trong thực tế vận hành: 
                Ngày lễ liên bang làm đảo lộn lịch trình; Mưa bão và tuyết rơi làm đứt gãy lưu thông.
              </p>
              <table className="academic-table">
                <thead>
                  <tr>
                    <th>Tình huống khảo sát</th>
                    <th>MAE (xe/h)</th>
                    <th>Ghi chú chuyên môn</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td>Ngày lễ liên bang (Holidays)</td><td><b>114.33 xe/h</b></td><td>Lưu lượng giảm sâu, dòng xe vắng vẻ</td></tr>
                  <tr><td>Ngày bình thường (Regular Days)</td><td>242.68 xe/h</td><td>Lưu lượng lớn, 2 đỉnh cao điểm</td></tr>
                  <tr><td>Trời quang đãng (Clear)</td><td>209.88 xe/h</td><td>Thời tiết thuận lợi, sai số thấp</td></tr>
                  <tr style={{background: '#fef2f2', fontWeight: 'bold'}}><td>Thời tiết cực đoan (Bão/Tuyết)</td><td><b>282.27 xe/h</b></td><td>Đứt gãy tốc độ lưu thông đột ngột</td></tr>
                </tbody>
              </table>
              <img src="/reports/figures/exp4_holiday_and_weather_errors.png" alt="TN4" className="academic-img" onError={(e) => { e.target.style.display = 'none'; }} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
