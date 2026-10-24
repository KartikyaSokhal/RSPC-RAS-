export default function RajasthanMap({ className = '' }) {
  return (
    <div className={`rajasthan-map-container ${className}`} aria-label="Vector illustration of Rajasthan state highlighting RPSC examination centers">
      <svg
        viewBox="0 0 600 560"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="rajasthan-vector-svg"
        role="img"
      >
        <title>Map of Rajasthan — Hub of RPSC RAS Examination</title>
        <desc>Stylized geographic boundary outline of Rajasthan highlighting Ajmer (RPSC HQ), Jaipur, Jodhpur, Udaipur, Bikaner, and Kota.</desc>

        <defs>
          {/* Subtle gradient fill for Rajasthan surface */}
          <linearGradient id="rajGradient" x1="120" y1="40" x2="480" y2="520" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="var(--primary)" stopOpacity="0.12" />
            <stop offset="50%" stopColor="var(--primary)" stopOpacity="0.06" />
            <stop offset="100%" stopColor="var(--primary)" stopOpacity="0.16" />
          </linearGradient>

          <filter id="mapShadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="6" stdDeviation="12" floodColor="var(--primary)" floodOpacity="0.15" />
          </filter>

          {/* Marker glow filter */}
          <filter id="pulseGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* GEOGRAPHIC STATE OUTLINE OF RAJASTHAN (Authentic rhomboid/kite polygon with natural boundaries) */}
        <path
          className="rajasthan-boundary"
          d="
            M 275,32
            C 290,30 320,45 338,58
            C 362,75 390,82 412,96
            C 434,110 460,118 478,136
            C 496,154 532,185 548,205
            C 560,220 545,238 528,252
            C 505,270 488,295 480,320
            C 472,345 485,370 492,392
            C 498,410 475,435 452,442
            C 430,448 405,420 388,435
            C 370,450 360,480 348,510
            C 338,535 315,548 295,538
            C 275,528 260,490 242,475
            C 225,460 200,452 182,438
            C 160,422 142,395 132,370
            C 122,345 105,320 85,295
            C 65,270 42,242 45,220
            C 48,198 80,182 108,165
            C 136,148 165,130 190,105
            C 215,80 245,45 275,32
            Z
          "
          fill="url(#rajGradient)"
          stroke="var(--primary)"
          strokeWidth="2.5"
          strokeLinejoin="round"
          strokeLinecap="round"
        />

        {/* ARAVALLI RANGE LINE (SW to NE diagonal mountain ridge, key physical feature of Rajasthan) */}
        <path
          className="aravalli-ridge"
          d="M 180,440 Q 260,330 330,270 T 425,120"
          stroke="var(--primary)"
          strokeWidth="1.75"
          strokeDasharray="4 6"
          strokeOpacity="0.45"
          fill="none"
        />
        <text x="215" y="375" transform="rotate(-42 215 375)" className="aravalli-label" fill="var(--muted)" fontSize="10" letterSpacing="2" fontWeight="600">
          ARAVALLI RANGE
        </text>

        {/* THAR DESERT LABEL (West) */}
        <text x="100" y="240" className="region-label" fill="var(--faint)" fontSize="11" letterSpacing="2.5" fontWeight="500">
          GREAT INDIAN DESERT
        </text>

        {/* KEY HUBS & CENTERS */}

        {/* 1. AJMER — RPSC HEADQUARTERS (Center) */}
        <g className="map-marker-hub rpsc-hq" transform="translate(325, 275)">
          <circle r="14" fill="var(--primary)" fillOpacity="0.18" className="pulse-ring" />
          <circle r="7" fill="var(--primary)" stroke="var(--surface)" strokeWidth="2" filter="url(#pulseGlow)" />
          <circle r="2.5" fill="var(--surface)" />
          <text x="16" y="4" className="marker-name hq-title" fill="var(--text)" fontSize="12" fontWeight="700">
            Ajmer
          </text>
          <text x="16" y="16" className="marker-sub" fill="var(--primary)" fontSize="9.5" fontWeight="600" letterSpacing="0.5">
            RPSC HEADQUARTERS
          </text>
        </g>

        {/* 2. JAIPUR — CAPITAL (East-Central) */}
        <g className="map-marker-hub" transform="translate(390, 225)">
          <circle r="5.5" fill="var(--text)" stroke="var(--surface)" strokeWidth="1.5" />
          <text x="12" y="4" className="marker-name" fill="var(--text)" fontSize="11" fontWeight="600">
            Jaipur
          </text>
        </g>

        {/* 3. JODHPUR — MARWAR (West-Central) */}
        <g className="map-marker-hub" transform="translate(220, 290)">
          <circle r="5" fill="var(--text)" stroke="var(--surface)" strokeWidth="1.5" />
          <text x="-12" y="4" textAnchor="end" className="marker-name" fill="var(--text)" fontSize="11" fontWeight="600">
            Jodhpur
          </text>
        </g>

        {/* 4. BIKANER — NORTH DESERT (North-West) */}
        <g className="map-marker-hub" transform="translate(230, 160)">
          <circle r="4.5" fill="var(--text)" stroke="var(--surface)" strokeWidth="1.5" />
          <text x="10" y="4" className="marker-name" fill="var(--text)" fontSize="10.5" fontWeight="500">
            Bikaner
          </text>
        </g>

        {/* 5. UDAIPUR — MEWAR (South) */}
        <g className="map-marker-hub" transform="translate(255, 435)">
          <circle r="5" fill="var(--text)" stroke="var(--surface)" strokeWidth="1.5" />
          <text x="12" y="4" className="marker-name" fill="var(--text)" fontSize="10.5" fontWeight="600">
            Udaipur
          </text>
        </g>

        {/* 6. KOTA — HADOTI (South-East) */}
        <g className="map-marker-hub" transform="translate(415, 380)">
          <circle r="4.5" fill="var(--text)" stroke="var(--surface)" strokeWidth="1.5" />
          <text x="10" y="4" className="marker-name" fill="var(--text)" fontSize="10.5" fontWeight="500">
            Kota
          </text>
        </g>
      </svg>
    </div>
  )
}
