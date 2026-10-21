import React from "react";

// Simple stroke icons drawn on a 64x64 grid so they stay crisp at any size.
type P = { size?: number; color?: string; stroke?: number };

const Svg: React.FC<P & { children: React.ReactNode }> = ({ size = 64, color = "currentColor", stroke = 3.5, children }) => (
  <svg width={size} height={size} viewBox="0 0 64 64" fill="none" stroke={color} strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round">
    {children}
  </svg>
);

export const HdbIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <rect x="14" y="6" width="36" height="52" rx="2" />
    {[14, 24, 34, 44].map((y) => (
      <g key={y}>
        <rect x="20" y={y} width="7" height="5" />
        <rect x="37" y={y} width="7" height="5" />
      </g>
    ))}
    <path d="M8 58h48" />
  </Svg>
);

export const LandedIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <path d="M8 30 32 10l24 20" />
    <path d="M14 26v30h36V26" />
    <rect x="27" y="40" width="10" height="16" />
    <path d="M6 58h52" />
  </Svg>
);

export const NonLandedIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <path d="M10 58V22l14-8v44" />
    <path d="M24 58V8l18 8v42" />
    <path d="M42 58V28l12 6v24" />
    <path d="M29 22h8M29 30h8M29 38h8M29 46h8" />
    <path d="M6 58h52" />
  </Svg>
);

export const RetailIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <path d="M8 22 13 8h38l5 14" />
    <path d="M8 22c0 4 3 7 8 7s8-3 8-7c0 4 3 7 8 7s8-3 8-7c0 4 3 7 8 7s8-3 8-7" />
    <path d="M12 29v29h40V29" />
    <rect x="20" y="38" width="10" height="20" />
    <rect x="36" y="38" width="10" height="9" />
  </Svg>
);

export const OfficeIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <rect x="10" y="20" width="44" height="34" rx="4" />
    <path d="M24 20v-6a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v6" />
    <path d="M10 34h44" />
    <path d="M28 34v5h8v-5" />
  </Svg>
);

export const IndustrialIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <path d="M6 58V30l14 8v-8l14 8v-8l14 8V14h8v44z" />
    <path d="M14 48h6M28 48h6M42 48h6" />
  </Svg>
);

export const BuildingIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <rect x="18" y="8" width="28" height="50" rx="2" />
    <path d="M24 16h4M36 16h4M24 24h4M36 24h4M24 32h4M36 32h4M24 40h4M36 40h4" />
    <path d="M28 58v-9h8v9" />
    <path d="M10 58h44" />
  </Svg>
);

export const SheetIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <path d="M14 6h26l12 12v40H14z" />
    <path d="M40 6v12h12" />
    <rect x="20" y="28" width="26" height="22" />
    <path d="M20 35h26M20 43h26M30 28v22" />
  </Svg>
);

export const GlobeIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <circle cx="32" cy="32" r="24" />
    <path d="M8 32h48M32 8c8 8 8 40 0 48M32 8c-8 8-8 40 0 48" />
  </Svg>
);

export const DirectoryIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <rect x="16" y="4" width="32" height="56" rx="6" />
    <rect x="21" y="12" width="22" height="10" rx="2" />
    <path d="M21 30h22M21 38h22M21 46h14" />
  </Svg>
);

export const SearchIcon: React.FC<P> = (p) => (
  <Svg {...p}>
    <circle cx="27" cy="27" r="16" />
    <path d="m39 39 15 15" />
  </Svg>
);
