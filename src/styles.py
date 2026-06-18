STYLES = """
<style>
    * { box-sizing: border-box; }
    body, html {
        margin: 0 !important;
        padding: 0 !important;
        background-color: #0b0c10 !important;
        overflow: hidden !important;
        width: 100vw;
        height: 100vh;
    }

    .dashboard-title {
        position: fixed;
        top: 0; left: 0; width: 100vw;
        padding: 10px 0; margin: 0 !important;
        font-size: 20px; font-weight: 900; letter-spacing: 4px;
        text-transform: uppercase; color: #66fcf1;
        background: #1f2833; text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.8);
        z-index: 9999;
    }

    #glowscript {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100vw;
        padding-top: 60px;
        padding-bottom: 60px;
    }
    
    canvas {
        width: 96vw !important;
        height: 75vh !important;
        max-width: calc(75vh * 21 / 9) !important;
        max-height: calc(96vw * 9 / 21) !important;
        box-shadow: 0px 0px 30px rgba(0, 0, 0, 0.9);
        border-radius: 8px;
        border: 1px solid #1f2833;
    }

    #slider-panel {
        position: fixed !important;
        top: 60px !important;
        left: 20px !important;
        background: rgba(31, 40, 51, 0.85) !important;
        border: 1px solid #45a29e !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #66fcf1 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.6) !important;
        z-index: 10000 !important;
        width: 290px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 14px !important;
    }

    .param-container {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
        width: 100% !important;
    }

    .param-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
    }

    .param-label {
        color: #c5c6c7 !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }

    .param-header span {
        color: #66fcf1 !important;
        font-weight: bold !important;
    }

    .ui-slider {
        background: #1f2833 !important;
        border: 1px solid #45a29e !important;
        height: 6px !important;
        border-radius: 3px !important;
        position: relative !important;
        margin: 6px 0 !important;
        cursor: pointer !important;
    }
    
    .ui-slider-handle {
        background: #66fcf1 !important;
        border: 1px solid #66fcf1 !important;
        width: 14px !important;
        height: 14px !important;
        border-radius: 50% !important;
        top: -5px !important;
        margin-left: -7px !important;
        cursor: pointer !important;
        box-shadow: 0 0 8px rgba(102, 252, 241, 0.8) !important;
        outline: none !important;
        position: absolute !important;
        z-index: 2 !important;
    }
    
    .ui-slider-handle:hover, .ui-slider-handle:focus {
        background: #45a29e !important;
        border-color: #45a29e !important;
        box-shadow: 0 0 12px #66fcf1 !important;
    }

    .ui-state-disabled {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
    }
    .ui-state-disabled .ui-slider-handle {
        cursor: not-allowed !important;
        background: #45a29e !important;
        border-color: #45a29e !important;
        box-shadow: none !important;
    }

    input[type=range] {
        -webkit-appearance: none !important;
        width: 100% !important;
        height: 6px !important;
        background: #1f2833 !important;
        border: 1px solid #45a29e !important;
        border-radius: 3px !important;
        outline: none !important;
        cursor: pointer !important;
        margin: 6px 0 !important;
    }
    input[type=range]::-webkit-slider-thumb {
        -webkit-appearance: none !important;
        width: 14px !important;
        height: 14px !important;
        border-radius: 50% !important;
        background: #66fcf1 !important;
        cursor: pointer !important;
        box-shadow: 0 0 8px rgba(102, 252, 241, 0.8) !important;
    }
    input[type=range][disabled] {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
    }

    #control-buttons {
        position: fixed !important;
        bottom: 15px !important;
        left: 0 !important;
        width: 100vw !important;
        display: flex !important;
        justify-content: center !important;
        gap: 15px !important;
        z-index: 10000 !important;
    }

    button {
        background-color: #1f2833 !important;
        color: #66fcf1 !important;
        border: 1px solid #45a29e !important;
        border-radius: 4px;
        padding: 10px 28px !important;
        margin: 0 !important;
        font-size: 14px !important;
        font-weight: bold;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    button:hover:not([disabled]) {
        background-color: #45a29e !important;
        color: #0b0c10 !important;
        box-shadow: 0px 0px 15px #66fcf1;
        transform: translateY(-2px);
    }

    button[disabled] {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    #control-buttons button:first-child:not([disabled]) {
        background-color: #0d3b2e !important;
        border-color: #66fcf1 !important;
        animation: pulse-glow 1.6s ease-in-out infinite;
    }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 8px rgba(102, 252, 241, 0.3); }
        50%       { box-shadow: 0 0 22px rgba(102, 252, 241, 0.75); }
    }

    .telemetry-panel {
        position: fixed !important;
        top: 60px !important;
        right: 20px !important;
        background: rgba(31, 40, 51, 0.85) !important;
        border: 1px solid #45a29e !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #66fcf1 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.6) !important;
        z-index: 10000 !important;
        width: 290px !important;
        pointer-events: none !important;
    }
    .telemetry-row {
        margin-bottom: 8px !important;
        display: flex !important;
        justify-content: space-between !important;
    }
    .telemetry-row:last-child { margin-bottom: 0 !important; }
    .telemetry-label {
        color: #c5c6c7 !important;
        font-weight: bold !important;
    }
    .telemetry-val {
        color: #66fcf1 !important;
        text-align: right !important;
    }
</style>
<div class="dashboard-title">Artemis II mission trajectory</div>
<script>
    (function() {
        function organizeLayout() {
            var panel = $("#slider-panel");
            if (panel.length) {
                var siblings = panel.nextAll();
                // We expect at least 6 widgets (3 labels + 3 sliders) to exist
                if (siblings.length >= 6) {
                    var w1 = siblings.eq(0);
                    var s1 = siblings.eq(1);
                    var w2 = siblings.eq(2);
                    var s2 = siblings.eq(3);
                    var w3 = siblings.eq(4);
                    var s3 = siblings.eq(5);

                    var c1 = $('<div class="param-container"></div>');
                    var h1 = $('<div class="param-header"><span class="param-label">Exit velocity:</span></div>').append(w1);
                    c1.append(h1, s1);

                    var c2 = $('<div class="param-container"></div>');
                    var h2 = $('<div class="param-header"><span class="param-label">Mission start angle:</span></div>').append(w2);
                    c2.append(h2, s2);

                    var c3 = $('<div class="param-container"></div>');
                    var h3 = $('<div class="param-header"><span class="param-label">Moon position angle:</span></div>').append(w3);
                    c3.append(h3, s3);

                    panel.append(c1, c2, c3);
                    
                    var controls = $("#control-buttons");
                    if (controls.length) {
                        var buttons = controls.nextAll("button");
                        controls.append(buttons);
                    }
                    
                    clearInterval(layoutInterval);
                }
            }
        }
        var layoutInterval = setInterval(organizeLayout, 50);
        setTimeout(function() { clearInterval(layoutInterval); }, 5000);
    })();
</script>
"""
