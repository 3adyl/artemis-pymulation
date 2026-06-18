def format_telemetry(telemetry_data, launched, sim_done, paused):
    """Format telemetry data as HTML for HUD display"""
    days = telemetry_data['days']
    hours = telemetry_data['hours']
    minutes = telemetry_data['minutes']
    seconds = telemetry_data['seconds']
    alt_e = telemetry_data['alt_e']
    vel_e = telemetry_data['vel_e']
    alt_m = telemetry_data['alt_m']
    vel_m = telemetry_data['vel_m']

    if not launched:
        status_color = '#f2a90b'
        status_text = 'AWAITING LAUNCH'
    elif sim_done:
        status_color = '#e83f3f'
        status_text = 'MISSION COMPLETE'
    elif paused:
        status_color = '#c5c6c7'
        status_text = 'PAUSED'
    else:
        status_color = '#66fcf1'
        status_text = 'IN FLIGHT'

    html = f"""
    <div class='telemetry-panel'>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Status:</span>
            <span class='telemetry-val' style='color:{status_color}'>{status_text}</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>MET:</span>
            <span class='telemetry-val'>{days:02d}d {hours:02d}h {minutes:02d}m {seconds:02d}s</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Altitude (Earth):</span>
            <span class='telemetry-val'>{alt_e:,.1f} km</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Velocity (Earth):</span>
            <span class='telemetry-val'>{vel_e:.3f} km/s</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Altitude (Moon):</span>
            <span class='telemetry-val'>{alt_m:,.1f} km</span>
        </div>
        <div class='telemetry-row'>
            <span class='telemetry-label'>Velocity (Moon):</span>
            <span class='telemetry-val'>{vel_m:.3f} km/s</span>
        </div>
    </div>
    """.replace(",", " ")

    return html
