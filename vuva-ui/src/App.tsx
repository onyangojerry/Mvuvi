import React, { useEffect, useMemo, useRef, useState } from "react";
import { WebSocketClient } from "./utils/websocketClient";
import * as THREE from "three";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { Stars, Html, OrbitControls } from "@react-three/drei";
import { create } from "zustand";

/**
 * Space News Universe
 * - Galaxies (topics) are big rotating clusters.
 * - Solar systems (subtopics) orbit within a galaxy.
 * - Planets (sub-subtopics) orbit around a solar system.
 * - Clicking filters the live feed (right HUD).
 */

// ---------------------------
// 1) Taxonomy (2026 categories)
// ---------------------------
const TAXONOMY = [
  {
    id: "politics",
    name: "Politics & Governance",
    systems: [
      {
        id: "elections",
        name: "Elections & Campaigns",
        planets: ["National Elections", "Election Administration", "Digital Campaign Ethics"],
      },
      {
        id: "geopolitics",
        name: "Geopolitics & Intl Affairs",
        planets: ["Global Alliances", "Lunar Exploration Rights", "Pax Silica Alliances"],
      },
      {
        id: "policy",
        name: "Public Policy",
        planets: ["Zoning & Land Use", "Medicaid Reform", "Transportation Funding"],
      },
    ],
  },
  {
    id: "economy",
    name: "Business & Economy",
    systems: [
      {
        id: "macro",
        name: "Macroeconomics",
        planets: ["K-Shaped Economy", "Sovereign Debt", "Central Bank Liquidity"],
      },
      {
        id: "geoecon",
        name: "Geoeconomics",
        planets: ["Rare Earth Supply Chains", "Export Controls", "Resilience Strategies"],
      },
      {
        id: "finance",
        name: "Industry & Finance",
        planets: ["AI Infrastructure Spend", "Data Center Energy", "ESG Standards"],
      },
    ],
  },
  {
    id: "tech",
    name: "Science & Technology",
    systems: [
      {
        id: "ai",
        name: "Artificial Intelligence",
        planets: ["Agentic AI", "Algorithmic Bias", "AI Misinformation", "AI Governance", "AI Slop"],
      },
      {
        id: "cyber",
        name: "Cybersecurity",
        planets: ["State-Linked Hacking", "Deepfake Verification", "Data Sovereignty", "Digital Resilience"],
      },
      {
        id: "frontier",
        name: "Space & Frontier Tech",
        planets: ["Commercial Lunar Missions", "Deep-Sea Mining", "Orbital Infrastructure"],
      },
    ],
  },
  {
    id: "health",
    name: "Health & Society",
    systems: [
      {
        id: "publichealth",
        name: "Public Health",
        planets: ["Mental Health", "Nutrition Assistance", "Medical Research"],
      },
      {
        id: "education",
        name: "Education",
        planets: ["Alternative Credentials", "AI-Era Curricula", "Misinformation Literacy"],
      },
      {
        id: "stories",
        name: "Human Stories & Diversity",
        planets: ["Queer Voices", "Black Voices", "Immigrant Community News"],
      },
    ],
  },
  {
    id: "climate",
    name: "Environment & Climate",
    systems: [
      {
        id: "impact",
        name: "Climate Impact",
        planets: ["Climate Migration", "Flood Insurance", "Ocean Conservation"],
      },
      {
        id: "energy",
        name: "Sustainability & Energy",
        planets: ["Renewable Energy", "GHG Monitoring", "Sustainable Business"],
      },
    ],
  },
  {
    id: "culture",
    name: "Lifestyle & Culture",
    systems: [
      {
        id: "ent",
        name: "Entertainment",
        planets: ["Music", "Film & Cinema", "Social Media Trends", "Performing Arts"],
      },
      {
        id: "sports",
        name: "Sports",
        planets: ["Winter Olympics 2026", "Men's T20 World Cup", "Player Profiles"],
      },
      {
        id: "life",
        name: "Personal Interest",
        planets: ["Travel Guides", "Food & Drink", "Parenting", "Home Living"],
      },
    ],
  },
];

// ---------------------------
// 2) Zustand store (navigation + filters + live feed)
// ---------------------------
const useUniverse = create((set, get) => ({
  selectedGalaxyId: null,
  selectedSystemId: null,
  selectedPlanet: null,
  shipMode: true,
  speed: 1.0,

  setSelection: (galaxyId, systemId = null, planet = null) =>
    set({ selectedGalaxyId: galaxyId, selectedSystemId: systemId, selectedPlanet: planet }),

  toggleShipMode: () => set({ shipMode: !get().shipMode }),

  news: [],
  pushNews: (item) => set({ news: [item, ...get().news].slice(0, 60) }),
  clearNews: () => set({ news: [] }),
}));

// ---------------------------
// 3) WebSocket real-time stream
// ---------------------------
function useNewsWebSocket(pushNews: (item: any) => void) {
  const wsRef = useRef<WebSocketClient | null>(null);
  const [status, setStatus] = useState<'connecting' | 'open' | 'closed' | 'error'>('connecting');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Optionally, get token from auth context or localStorage
    const token = localStorage.getItem('auth_token') || undefined;
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.hostname}:8000/api/v1/feed/stream`;
    wsRef.current = new WebSocketClient({
      url: wsUrl,
      token,
      onMessage: (msg) => {
        if (msg.type === 'news' && msg.article) {
          pushNews(msg.article);
        }
      },
      onOpen: () => {
        setStatus('open');
        setError(null);
      },
      onError: (e) => {
        setStatus('error');
        setError('WebSocket error');
      },
      onClose: (ev) => {
        setStatus('closed');
        if (!ev.wasClean) setError('WebSocket closed unexpectedly');
      },
      reconnect: true,
      reconnectIntervalMs: 3000,
      maxReconnectAttempts: 10,
    });
    return () => {
      wsRef.current?.close();
    };
  }, [pushNews]);

  return { status, error };
}

// ---------------------------
// 4) 3D helpers
// ---------------------------
function lerp(a, b, t) {
  return a + (b - a) * t;
}

function smoothDampVec3(current, target, lambda, dt) {
  current.x = lerp(current.x, target.x, 1 - Math.exp(-lambda * dt));
  current.y = lerp(current.y, target.y, 1 - Math.exp(-lambda * dt));
  current.z = lerp(current.z, target.z, 1 - Math.exp(-lambda * dt));
}

// ---------------------------
// 5) Spaceship camera controller (WASD + warp-to-selection)
// ---------------------------
function ShipController() {
  const { camera } = useThree();
  const { selectedGalaxyId, shipMode, speed } = useUniverse();
  const vel = useRef(new THREE.Vector3(0, 0, 0));
  const keys = useRef({ w: false, a: false, s: false, d: false, shift: false });

  useEffect(() => {
    const down = (e) => {
      if (e.key === "w") keys.current.w = true;
      if (e.key === "a") keys.current.a = true;
      if (e.key === "s") keys.current.s = true;
      if (e.key === "d") keys.current.d = true;
      if (e.key === "Shift") keys.current.shift = true;
    };
    const up = (e) => {
      if (e.key === "w") keys.current.w = false;
      if (e.key === "a") keys.current.a = false;
      if (e.key === "s") keys.current.s = false;
      if (e.key === "d") keys.current.d = false;
      if (e.key === "Shift") keys.current.shift = false;
    };
    window.addEventListener("keydown", down);
    window.addEventListener("keyup", up);
    return () => {
      window.removeEventListener("keydown", down);
      window.removeEventListener("keyup", up);
    };
  }, []);

  useFrame((_, dt) => {
    if (!shipMode) return;

    const accel = (keys.current.shift ? 18 : 10) * speed;
    const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
    const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);

    const a = new THREE.Vector3(0, 0, 0);
    if (keys.current.w) a.add(forward);
    if (keys.current.s) a.addScaledVector(forward, -1);
    if (keys.current.d) a.add(right);
    if (keys.current.a) a.addScaledVector(right, -1);

    if (a.lengthSq() > 0) a.normalize().multiplyScalar(accel);

    vel.current.addScaledVector(a, dt);
    vel.current.multiplyScalar(Math.pow(0.02, dt));

    camera.position.addScaledVector(vel.current, dt);

    if (selectedGalaxyId) {
      const idx = TAXONOMY.findIndex((g) => g.id === selectedGalaxyId);
      if (idx >= 0) {
        const target = new THREE.Vector3(0, 0, 0);
        const ringR = 28;
        const theta = (idx / TAXONOMY.length) * Math.PI * 2;
        target.set(Math.cos(theta) * ringR, 0, Math.sin(theta) * ringR);
        const desired = target.clone().add(new THREE.Vector3(0, 6, 18));
        smoothDampVec3(camera.position, desired, 2.2, dt);
        camera.lookAt(target);
      }
    }
  });

  return null;
}

// ---------------------------
// 6) Galaxy rendering
// ---------------------------
function Galaxy({ galaxy, index }) {
  const group = useRef();
  const { selectedGalaxyId, setSelection } = useUniverse();

  const ringR = 28;
  const theta = (index / TAXONOMY.length) * Math.PI * 2;

  const basePos = useMemo(() => {
    const x = Math.cos(theta) * ringR;
    const z = Math.sin(theta) * ringR;
    return new THREE.Vector3(x, 0, z);
  }, [theta]);

  const particles = useMemo(() => {
    const pts = [];
    const arms = 3;
    const count = 380;

    for (let i = 0; i < count; i++) {
      const t = i / count;
      const arm = i % arms;
      const angle = t * Math.PI * 6 + (arm * (Math.PI * 2)) / arms;
      const radius = 1.8 + t * 6.5;
      const y = (Math.random() - 0.5) * 1.2;
      pts.push(
        new THREE.Vector3(
          Math.cos(angle) * radius + (Math.random() - 0.5) * 0.35,
          y,
          Math.sin(angle) * radius + (Math.random() - 0.5) * 0.35
        )
      );
    }
    return pts;
  }, []);

  useFrame((_, dt) => {
    if (!group.current) return;
    group.current.position.copy(basePos);
    group.current.rotation.y += dt * 0.12;
  });

  const isSelected = selectedGalaxyId === galaxy.id;

  return (
    <group ref={group}>
      <mesh
        onClick={(e) => {
          e.stopPropagation();
          setSelection(galaxy.id, null, null);
        }}
      >
        <sphereGeometry args={[isSelected ? 1.8 : 1.35, 32, 32]} />
        <meshStandardMaterial emissiveIntensity={1.1} emissive={new THREE.Color(0xffffff)} color={new THREE.Color(0x0b1022)} />
      </mesh>

      <Html distanceFactor={18} position={[0, 3.0, 0]} style={{ pointerEvents: "none" }}>
        <div
          style={{
            fontFamily: "ui-sans-serif, system-ui",
            color: "white",
            letterSpacing: 0.3,
            padding: "6px 10px",
            borderRadius: 10,
            background: "rgba(0,0,0,0.45)",
            border: "1px solid rgba(255,255,255,0.18)",
            whiteSpace: "nowrap",
          }}
        >
          {galaxy.name}
          <span style={{ opacity: 0.7, marginLeft: 10 }}>({galaxy.systems.length} systems)</span>
        </div>
      </Html>

      {particles.map((p, i) => (
        <mesh
          key={i}
          position={[p.x, p.y, p.z]}
          onPointerOver={(e) => e.stopPropagation()}
          onClick={(e) => {
            e.stopPropagation();
            setSelection(galaxy.id, null, null);
          }}
        >
          <sphereGeometry args={[0.06, 10, 10]} />
          <meshStandardMaterial emissiveIntensity={0.9} emissive={new THREE.Color(0xffffff)} color={new THREE.Color(0x111827)} />
        </mesh>
      ))}

      {isSelected &&
        galaxy.systems.map((sys, sIdx) => (
          <SolarSystem key={sys.id} galaxy={galaxy} system={sys} systemIndex={sIdx} />
        ))}
    </group>
  );
}

function SolarSystem({ galaxy, system, systemIndex }) {
  const group = useRef();
  const { selectedSystemId, setSelection } = useUniverse();

  const radius = 7.5 + systemIndex * 3.8;
  const speed = 0.25 + systemIndex * 0.05;

  useFrame(({ clock }) => {
    if (!group.current) return;
    const t = clock.getElapsedTime() * speed;
    group.current.position.set(Math.cos(t) * radius, 0.6 * Math.sin(t * 0.7), Math.sin(t) * radius);
    group.current.rotation.y += 0.02;
  });

  const isSelected = selectedSystemId === system.id;

  return (
    <group ref={group}>
      <mesh
        onClick={(e) => {
          e.stopPropagation();
          setSelection(galaxy.id, system.id, null);
        }}
      >
        <sphereGeometry args={[isSelected ? 0.9 : 0.7, 24, 24]} />
        <meshStandardMaterial emissiveIntensity={1.2} emissive={new THREE.Color(0xffffff)} color={new THREE.Color(0x0b1022)} />
      </mesh>

      <Html distanceFactor={25} position={[0, 1.6, 0]} style={{ pointerEvents: "none" }}>
        <div
          style={{
            fontFamily: "ui-sans-serif, system-ui",
            color: "white",
            padding: "4px 8px",
            borderRadius: 10,
            background: "rgba(0,0,0,0.35)",
            border: "1px solid rgba(255,255,255,0.14)",
            fontSize: 12,
            whiteSpace: "nowrap",
          }}
        >
          {system.name}
        </div>
      </Html>

      {system.planets.map((planet, pIdx) => (
        <Planet
          key={planet}
          galaxyId={galaxy.id}
          systemId={system.id}
          planet={planet}
          index={pIdx}
          orbitRadius={1.8 + pIdx * 0.95}
        />
      ))}
    </group>
  );
}

function Planet({ galaxyId, systemId, planet, index, orbitRadius }) {
  const mesh = useRef();
  const { selectedPlanet, setSelection } = useUniverse();
  const speed = 0.7 + index * 0.18;

  useFrame(({ clock }) => {
    if (!mesh.current) return;
    const t = clock.getElapsedTime() * speed;
    mesh.current.position.set(Math.cos(t) * orbitRadius, 0.12 * Math.sin(t * 1.3), Math.sin(t) * orbitRadius);
    mesh.current.rotation.y += 0.04;
  });

  const isSelected = selectedPlanet === planet;

  return (
    <mesh
      ref={mesh}
      onClick={(e) => {
        e.stopPropagation();
        setSelection(galaxyId, systemId, planet);
      }}
    >
      <sphereGeometry args={[isSelected ? 0.28 : 0.22, 18, 18]} />
      <meshStandardMaterial emissiveIntensity={0.7} emissive={new THREE.Color(0xffffff)} color={new THREE.Color(0x0b1022)} />
      <Html distanceFactor={40} position={[0, 0.6, 0]} style={{ pointerEvents: "none" }}>
        <div
          style={{
            fontFamily: "ui-sans-serif, system-ui",
            color: "white",
            fontSize: 11,
            opacity: 0.9,
            padding: "2px 6px",
            borderRadius: 999,
            background: "rgba(0,0,0,0.28)",
            border: "1px solid rgba(255,255,255,0.12)",
            whiteSpace: "nowrap",
          }}
        >
          {planet}
        </div>
      </Html>
    </mesh>
  );
}

// ---------------------------
// 7) HUD (filters + feed)
// ---------------------------
function Hud() {
  const {
    selectedGalaxyId,
    selectedSystemId,
    selectedPlanet,
    setSelection,
    shipMode,
    toggleShipMode,
    news,
    clearNews,
  } = useUniverse();

  const selectedGalaxy = TAXONOMY.find((g) => g.id === selectedGalaxyId) || null;
  const selectedSystem =
    selectedGalaxy?.systems?.find((s) => s.id === selectedSystemId) || null;

  const filtered = useMemo(() => {
    return news.filter((n) => {
      if (selectedGalaxyId && n.galaxyId !== selectedGalaxyId) return false;
      if (selectedSystemId && n.systemId !== selectedSystemId) return false;
      if (selectedPlanet && n.planet !== selectedPlanet) return false;
      return true;
    });
  }, [news, selectedGalaxyId, selectedSystemId, selectedPlanet]);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        display: "grid",
        gridTemplateColumns: "340px 1fr 420px",
        gap: 16,
        padding: 16,
      }}
    >
      {/* Left HUD: Navigation */}
      <div
        style={{
          pointerEvents: "auto",
          background: "rgba(0,0,0,0.45)",
          border: "1px solid rgba(255,255,255,0.14)",
          borderRadius: 16,
          padding: 14,
          height: "fit-content",
          backdropFilter: "blur(8px)",
        }}
      >
        <div style={{ color: "white", fontFamily: "ui-sans-serif, system-ui", fontWeight: 700, fontSize: 14 }}>
          Navigation Console
        </div>
        <div style={{ color: "rgba(255,255,255,0.75)", fontFamily: "ui-sans-serif, system-ui", fontSize: 12, marginTop: 6 }}>
          Click a galaxy → a system → a planet to filter. WASD + Shift to fly. Click empty space to clear.
        </div>

        <div style={{ display: "flex", gap: 8, marginTop: 10, flexWrap: "wrap" }}>
          <button onClick={toggleShipMode} style={btn()}>
            {shipMode ? "Ship Mode: ON" : "Ship Mode: OFF"}
          </button>
          <button onClick={() => setSelection(null, null, null)} style={btn()}>
            Clear Selection
          </button>
          <button onClick={clearNews} style={btn()}>
            Clear Feed
          </button>
        </div>

        <div style={{ marginTop: 12, paddingTop: 10, borderTop: "1px solid rgba(255,255,255,0.12)" }}>
          <div style={smallLabel()}>Current Focus</div>
          <div style={smallValue()}>{selectedGalaxy?.name || "—"}</div>
          <div style={smallValue()}>{selectedSystem?.name || "—"}</div>
          <div style={smallValue()}>{selectedPlanet || "—"}</div>
        </div>

        <div style={{ marginTop: 12 }}>
          <div style={smallLabel()}>Jump to Galaxy</div>
          <div style={{ display: "grid", gap: 8, marginTop: 8 }}>
            {TAXONOMY.map((g) => (
              <button key={g.id} onClick={() => setSelection(g.id, null, null)} style={btn({ textAlign: "left" })}>
                {g.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Center overlay is empty (3D scene) */}
      <div />

      {/* Right HUD: Live Feed */}
      <div
        style={{
          pointerEvents: "auto",
          background: "rgba(0,0,0,0.45)",
          border: "1px solid rgba(255,255,255,0.14)",
          borderRadius: 16,
          padding: 14,
          backdropFilter: "blur(8px)",
          maxHeight: "calc(100vh - 32px)",
          overflow: "auto",
        }}
      >
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 12 }}>
          <div style={{ color: "white", fontFamily: "ui-sans-serif, system-ui", fontWeight: 800, fontSize: 14 }}>
            Live Stream
          </div>
          <div style={{ color: "rgba(255,255,255,0.7)", fontFamily: "ui-sans-serif, system-ui", fontSize: 12 }}>
            Showing {filtered.length}/{news.length}
          </div>
        </div>

        <div style={{ color: "rgba(255,255,255,0.75)", fontFamily: "ui-sans-serif, system-ui", fontSize: 12, marginTop: 6 }}>
          {selectedGalaxy || selectedSystem || selectedPlanet ? (
            <>Filtered to your current "flight path".</>
          ) : (
            <>Unfiltered: the full universe feed.</>
          )}
        </div>

        <div style={{ display: "grid", gap: 10, marginTop: 12 }}>
          {filtered.map((n) => (
            <div
              key={n.id}
              style={{
                borderRadius: 14,
                border: "1px solid rgba(255,255,255,0.12)",
                background: "rgba(10,14,28,0.55)",
                padding: 12,
              }}
            >
              <div style={{ color: "white", fontFamily: "ui-sans-serif, system-ui", fontWeight: 700, fontSize: 13, lineHeight: 1.25 }}>
                {n.title}
              </div>
              <div style={{ marginTop: 6, color: "rgba(255,255,255,0.72)", fontFamily: "ui-sans-serif, system-ui", fontSize: 12, lineHeight: 1.3 }}>
                {n.summary}
              </div>

              <div style={{ marginTop: 8, display: "flex", gap: 8, flexWrap: "wrap" }}>
                <span style={tag()}>{n.galaxyId}</span>
                <span style={tag()}>{n.systemId}</span>
                <span style={tag()}>{n.planet}</span>
              </div>

              <div style={{ marginTop: 8, color: "rgba(255,255,255,0.6)", fontFamily: "ui-sans-serif, system-ui", fontSize: 11 }}>
                {new Date(n.ts).toLocaleString()} · {n.source}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function btn(extra = {}) {
  return {
    pointerEvents: "auto",
    cursor: "pointer",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.16)",
    background: "rgba(10,14,28,0.55)",
    color: "white",
    padding: "8px 10px",
    fontFamily: "ui-sans-serif, system-ui",
    fontSize: 12,
    ...extra,
  };
}

function tag() {
  return {
    color: "rgba(255,255,255,0.75)",
    border: "1px solid rgba(255,255,255,0.14)",
    background: "rgba(0,0,0,0.25)",
    borderRadius: 999,
    padding: "2px 8px",
    fontFamily: "ui-sans-serif, system-ui",
    fontSize: 11,
  };
}

function smallLabel() {
  return { color: "rgba(255,255,255,0.6)", fontFamily: "ui-sans-serif, system-ui", fontSize: 11 };
}
function smallValue() {
  return { color: "white", fontFamily: "ui-sans-serif, system-ui", fontSize: 12, marginTop: 3 };
}

// ---------------------------
// 8) Main component
// ---------------------------
  const pushNews = useUniverse((s) => s.pushNews);
  const { status, error } = useNewsWebSocket(pushNews);

  return (
    <div style={{ width: "100vw", height: "100vh", background: "#050712" }}>
      <Canvas camera={{ position: [0, 8, 42], fov: 55 }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[20, 25, 18]} intensity={1.2} />
        <Stars radius={140} depth={40} count={5000} factor={4} saturation={0} fade speed={1} />

        <ShipController />
        <OrbitControls enablePan={false} enableDamping dampingFactor={0.08} rotateSpeed={0.4} />

        <mesh
          onClick={() => useUniverse.getState().setSelection(null, null, null)}
          position={[0, -8, 0]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <planeGeometry args={[600, 600]} />
          <meshBasicMaterial transparent opacity={0} />
        </mesh>

        {TAXONOMY.map((g, idx) => (
          <Galaxy key={g.id} galaxy={g} index={idx} />
        ))}
      </Canvas>

      <Hud />
      <div style={{position:'absolute',top:10,right:10,zIndex:1000}}>
        {status === 'connecting' && <span style={{color:'#ff0'}}>Connecting to live news…</span>}
        {status === 'error' && <span style={{color:'#f00'}}>WebSocket error: {error}</span>}
        {status === 'closed' && <span style={{color:'#f00'}}>WebSocket disconnected</span>}
      </div>
    </div>
  );
}