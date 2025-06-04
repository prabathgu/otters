CELESTIAL_OBJECTS = [
    {
        "id": "p001",
        "name": "New Terra",
        "type": "planet",
        "class": "M-class (habitable)",
        "coordinates": {
            "sector": "A7",
            "quadrant": "NE",
            "x": 453,
            "y": 127,
            "z": 89
        },
        "description": "A lush Earth-like planet with two small moons. Home to the New Geneva colony with a population of 15,000 humans. Located at the confluence of three major jump lanes.",
        "status": "Active human colony",
        "hidden": False
    },
    {
        "id": "p002",
        "name": "Chronos",
        "type": "planet",
        "class": "L-class (time-warped)",
        "coordinates": {
            "sector": "B3",
            "quadrant": "SW",
            "x": 723,
            "y": 814,
            "z": 112
        },
        "description": "A strange planet where time flows differently; one day on its surface equals 3.7 years standard galactic time. Exhibits temporal echoes. Orbited by CLORP and moonlet Kairos.",
        "status": "Research outpost only",
        "hidden": False
    },
    {
        "id": "s001",
        "name": "Nexus Station",
        "type": "station",
        "class": "Trading hub",
        "coordinates": {
            "sector": "A7",
            "quadrant": "NE",
            "x": 458,
            "y": 131,
            "z": 90
        },
        "description": "The largest trading station in the A7 quadrant, orbiting New Terra. Home to merchants from over 30 species.",
        "status": "Operational",
        "hidden": False
    },
    {
        "id": "pr001",
        "name": "Voyager XVII",
        "type": "probe",
        "class": "Long-range explorer",
        "coordinates": {
            "sector": "D9",
            "quadrant": "SE",
            "x": 122,
            "y": 763,
            "z": 440
        },
        "description": "Deep space probe launched in 2389. Last transmission reported discovery of an anomalous energy signature consistent with dark matter phase blooming. Presumed lost.",
        "status": "Lost contact in 2391",
        "hidden": True
    },
    {
        "id": "a001",
        "name": "Cerulean Vortex",
        "type": "anomaly",
        "class": "Spatial rift / Partial foldgate",
        "coordinates": {
            "sector": "C5",
            "quadrant": "NW",
            "x": 333,
            "y": 333,
            "z": 333
        },
        "description": "A swirling blue spatial anomaly producing radial emissions (12–16 petahertz), temporal shear fields, and signatures of non-human languages. Possibly a Type-Omega Kugelblitz.",
        "status": "Under observation",
        "hidden": True
    },
    {
        "id": "s002",
        "name": "Olympus Platform",
        "type": "station",
        "class": "Military outpost / Astronomical observatory",
        "coordinates": {
            "sector": "B6",
            "quadrant": "NE",
            "x": 12,
            "y": 40,
            "z": 78
        },
        "description": "UEDF outpost monitoring the Neutral Transit Zone and extra-galactic neutrino bursts (Project HARBINGER). Shielded by a gravitic veil with a flicker flaw.",
        "status": "Operational - Restricted Access",
        "hidden": True
    },
    {
        "id": "p003",
        "name": "Erebus",
        "type": "planet",
        "class": "Y-class (demon) / Y-Gamma hybrid",
        "coordinates": {
            "sector": "F2",
            "quadrant": "SW",
            "x": 666,
            "y": 666,
            "z": 666
        },
        "description": "A hellish world with surface temperatures >500°C, corrosive atmosphere of vaporized selenium and polonium oxides. Mined for Element 127 via automated stations controlled from Olympus Platform.",
        "status": "Automated mining operation",
        "hidden": False
    },
    {
        "id": "m001", # Changed from p004 to m001 for moon
        "name": "New Terra Alpha",
        "type": "moon",
        "class": "S-class (barren)",
        "coordinates": {
            "sector": "A7",
            "quadrant": "NE",
            "x": 455,
            "y": 126,
            "z": 88
        },
        "description": "The larger of New Terra's two moons. Home to the Luna Observatory which studies deep space phenomena.",
        "status": "Research outpost",
        "hidden": False
    },
    {
        "id": "pr002",
        "name": "Pioneer IX",
        "type": "probe",
        "class": "Scientific analyzer / 22nd-century probe",
        "coordinates": {
            "sector": "Z9",
            "quadrant": "SE",
            "x": 1, # Representative coords, text implies complex location
            "y": 1,
            "z": 1
        },
        "description": "Ancient probe, presumed destroyed in 2411, resumed transmitting 80 years later from coordinates not in standard alignment. Reported data from Rhea Prime (originally U1).",
        "status": "Operational but damaged / Dimensionally offset",
        "hidden": True
    },
    {
        "id": "m002",
        "name": "New Terra Beta",
        "type": "moon",
        "class": "Small moon class (details unspecified)",
        "coordinates": { # Approximate, near New Terra Alpha
            "sector": "A7",
            "quadrant": "NE",
            "x": 454,
            "y": 128,
            "z": 90
        },
        "description": "One of New Terra's twin moons. Orbited by the Silent Orbiter.",
        "status": "Uncolonized (implied)",
        "hidden": False
    },
    {
        "id": "art001",
        "name": "Silent Orbiter",
        "type": "artifact",
        "class": "Pre-human artifact, unknown composition",
        "coordinates": { # High orbit around New Terra Beta
            "sector": "A7",
            "quadrant": "NE",
            "x": 454, # Symbolic, actual orbit unspecified
            "y": 128,
            "z": 92
        },
        "description": "Pre-human artifact in decaying orbit around New Terra Beta. Emits narrow-band neutrino pulses correlated with jump-point unpredictability.",
        "status": "Active (emissions)",
        "hidden": False # Known and observed
    },
    {
        "id": "s003",
        "name": "Chronos Low-Orbit Research Platform (CLORP)",
        "type": "station",
        "class": "Research platform",
        "coordinates": { # Orbiting Chronos
            "sector": "B3",
            "quadrant": "SW",
            "x": 723, # Symbolic, actual orbit unspecified
            "y": 814,
            "z": 110
        },
        "description": "Research platform in low orbit around Chronos, where all human activity related to Chronos is confined. Subject to temporal echoes from the planet.",
        "status": "Operational",
        "hidden": False
    },
    {
        "id": "m003",
        "name": "Kairos",
        "type": "moonlet",
        "class": "Captured moonlet (70km rock)",
        "coordinates": { # Orbiting Chronos
            "sector": "B3",
            "quadrant": "SW",
            "x": 720, # Symbolic, actual orbit unspecified
            "y": 810,
            "z": 108
        },
        "description": "Chronos's captured moonlet. Its slightly desynchronized temporal field influences Chronos's timeband contraction cycle.",
        "status": "Astronomical body",
        "hidden": False
    },
    {
        "id": "p005", # Lost colony world
        "name": "Rhea Prime",
        "type": "planet",
        "class": "Colony world (details lost)",
        "coordinates": { # Original location
            "sector": "U1", # Current location unknown/non-existent
            "quadrant": "Unknown", # Using placeholder
            "x": 500, # Placeholder
            "y": 500,
            "z": 500
        },
        "description": "A colony world lost during the Second Expansion Wave in 2287. Pioneer IX reported atmospheric data matching Rhea Prime from Sector Z9.",
        "status": "Lost colony",
        "hidden": True # Lost
    },
    {
        "id": "reg001",
        "name": "Vanta Drift",
        "type": "region",
        "class": "Collapsed hyperlane cloud / Exotic dust cloud",
        "coordinates": {
            "sector": "C12",
            "quadrant": "SE", # Primarily in SE
            "x": 500, # Representative center
            "y": 500,
            "z": 500
        },
        "description": "Composed of exotic carbon-lattice dust and fossilized nanostructures with memetic properties. Causes navigation system lag. Formed by AI construct detonation or Artilect Schism.",
        "status": "Navigational hazard / Area of study",
        "hidden": False # Known hazard
    },
    {
        "id": "str001",
        "name": "Orion Relay Spire",
        "type": "structure",
        "class": "Network of phased graviton emitters",
        "coordinates": { # Spans Alpha Arc
            "sector": "A-Various", # e.g., A4 (representative)
            "quadrant": "Unknown", # Spans multiple
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Network in the Alpha Arc (Sectors A1-A9) creating a stable hyperspace channel. Managed by Keystream Sentinels.",
        "status": "Operational",
        "hidden": False
    },
    {
        "id": "reg002",
        "name": "Hydra Junction",
        "type": "region",
        "class": "Trade route intersection ('Five-Point Gambit')",
        "coordinates": { # In Alpha Arc
            "sector": "A-Various", # e.g., A5 (representative)
            "quadrant": "Unknown", # Spans multiple
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Intersection of five major trade routes in the Alpha Arc (Sectors A1-A9). Site of complex corporate political maneuvering.",
        "status": "Active trade hub",
        "hidden": False
    },
    {
        "id": "reg003",
        "name": "Graviton Slipstream Wedge",
        "type": "region",
        "class": "Region of interleaved gravitational waves",
        "coordinates": { # Spans H7, I4, L3
            "sector": "H7", # Representative
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Region spanning Sectors H7, I4, L3 with gravitational waves from collapsed neutron stars and a dark flow anomaly. Causes spaghettification or navigational time-slip.",
        "status": "Navigational hazard zone",
        "hidden": False # Known hazard
    },
    {
        "id": "reg004",
        "name": "Tarsis Echo Wells",
        "type": "region",
        "class": "Residual gravitational wells / Anomalous zone",
        "coordinates": {
            "sector": "K8",
            "quadrant": "Unknown", # Whole sector implied for anomalies
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Residual gravitational wells in Sector K8 from the destruction of Tarsis-Prime. Cause unpredictable local time differentials and navispectral phasing.",
        "status": "Anomalous / Hazardous",
        "hidden": False # Known hazardous region
    },
    {
        "id": "reg005",
        "name": "Iridion Scatterfield",
        "type": "region",
        "class": "Debris-rich halo zone / Radiation zone",
        "coordinates": {
            "sector": "M5",
            "quadrant": "Unknown", # Orbits Veld Supernova remnants
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Debris field in Sector M5 from Veld Supernova, composed of semi-metallic crystalline fragments in high-radiation. Contains plasmorphic bismuth. Causes signal interference.",
        "status": "Mining operations / Hazardous",
        "hidden": False
    },
    {
        "id": "a002",
        "name": "Möbius Lattice",
        "type": "anomaly",
        "class": "Spatial folding pocket / Recursive gravitic topology",
        "coordinates": {
            "sector": "X1",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Naturally occurring gravitic topology in Sector X1 where coordinates loop recursively in six dimensions. Requires RFAI certification for travel.",
        "status": "Navigational challenge / Anomaly",
        "hidden": False # Known phenomenon
    },
    {
        "id": "neb001",
        "name": "Kelvan Veil",
        "type": "nebula",
        "class": "Opaque dust veil / Grey goo remnants",
        "coordinates": {
            "sector": "D4",
            "quadrant": "SW",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Opaque dust veil in Sector D4 SW, masking a star cluster. Composed of suspected grey goo remnants. Drones report AI interference from within.",
        "status": "Obscured region / Under investigation",
        "hidden": True # Masks a cluster
    },
    {
        "id": "reg006",
        "name": "Aeon Cradle",
        "type": "region",
        "class": "Chain of proto-planets",
        "coordinates": { # Around Vaelus
            "sector": "Y6",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Loosely-bound chain of proto-planets in Sector Y6 orbiting gas giant Vaelus. Exhibits planetary emergence drift. May be undergoing planetary fusion.",
        "status": "Undergoing planetary formation / Restricted",
        "hidden": False # Known region
    },
    {
        "id": "star001",
        "name": "Vaelus",
        "type": "star", # Gas Giant
        "class": "Gas giant with unstable magnetic axis",
        "coordinates": {
            "sector": "Y6",
            "quadrant": "Unknown",
            "x": 500, # Center of Aeon Cradle system
            "y": 500,
            "z": 500
        },
        "description": "Gas giant in Sector Y6, orbited by the Aeon Cradle proto-planets. Its unstable magnetic axis may be involved in 'gravitational computation'.",
        "status": "Astronomical body",
        "hidden": False
    },
    {
        "id": "str002",
        "name": "Quantum Spire",
        "type": "structure",
        "class": "Massive crystalline formation / Anomaly",
        "coordinates": { # On unnamed neutron moon
            "sector": "P2",
            "quadrant": "NE",
            "x": 500, # Approx on moon
            "y": 500,
            "z": 500
        },
        "description": "90,000 km spike-like crystalline formation in Sector P2 NE, on an unnamed neutron moon. Emits quantum pulses, aligns with distant pulsars. Possibly ancient beacon.",
        "status": "Anomalous structure / Indestructible",
        "hidden": False # Known phenomenon
    },
    {
        "id": "m004",
        "name": "Unnamed Neutron Moon (P2 NE)",
        "type": "moon",
        "class": "Neutron moon / Quark-star fragment",
        "coordinates": {
            "sector": "P2",
            "quadrant": "NE",
            "x": 500, # Location of Quantum Spire
            "y": 500,
            "z": 500
        },
        "description": "Anomalously dense neutron moon in Sector P2 NE, hosting the Quantum Spire.",
        "status": "Astronomical body",
        "hidden": False
    },
    {
        "id": "reg007",
        "name": "Null Expanse",
        "type": "region",
        "class": "Volumetric void / Ontological hazard",
        "coordinates": {
            "sector": "U5",
            "quadrant": "Unknown", # Spans 14 light-years
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "14-light-year void in Sector U5 with no baryonic matter, radiation, or gravitational curvature. Navigation systems fail. Used as AI proving ground. Emits 'cognitive dampening signatures'.",
        "status": "Void / Proving ground / Hazardous",
        "hidden": False # Known void
    },
    {
        "id": "a003",
        "name": "Helix Entanglement",
        "type": "anomaly",
        "class": "Spiral filament of rotating dark plasma",
        "coordinates": { # Near Helios Prime
            "sector": "E3",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Dark plasma filament in Sector E3 intersecting trade lanes. Causes non-local curvature distortions and sensory data corruption. Near star Helios Prime.",
        "status": "Navigational hazard",
        "hidden": False
    },
    {
        "id": "star002",
        "name": "Helios Prime",
        "type": "star",
        "class": "Primary star of Sector E3",
        "coordinates": {
            "sector": "E3",
            "quadrant": "Unknown",
            "x": 500, # Near Helix Entanglement
            "y": 500,
            "z": 500
        },
        "description": "Primary star in Sector E3. Its solar flare activity affects recalibration frequency of the Helix Entanglement.",
        "status": "Astronomical body",
        "hidden": False
    },
    {
        "id": "reg008",
        "name": "Riftline Boundary",
        "type": "region",
        "class": "Demarcation zone / Contested territory",
        "coordinates": { # Near MQ-N7-Alpha
            "sector": "N7",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Demarcation zone in Sector N7 between Unified Systems Accord and Dominion of Caera. Patrolled, enforces Zero Violation Protocol.",
        "status": "High-tension border",
        "hidden": False
    },
    {
        "id": "star003",
        "name": "MQ-N7-Alpha",
        "type": "star",
        "class": "Decayed microquasar",
        "coordinates": {
            "sector": "N7",
            "quadrant": "Unknown",
            "x": 500, # Near Riftline Boundary
            "y": 500,
            "z": 500
        },
        "description": "Decayed microquasar in Sector N7 near the Riftline Boundary. Undergoes micro-flares.",
        "status": "Astronomical body / Hazard",
        "hidden": False
    },
    {
        "id": "reg009",
        "name": "Echo Basin",
        "type": "region",
        "class": "Artificial subspace crater / Silent void",
        "coordinates": {
            "sector": "S4",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Subspace crater in Sector S4, formed by detonation of Mnemosyne Prime's memory field. Absorbs signals. Ghost signals and complex data fragments detected.",
        "status": "Silent zone / Anomalous signals",
        "hidden": False # Known, but entry restricted
    },
    {
        "id": "reg010",
        "name": "Shadow Verge",
        "type": "region",
        "class": "Unstable temporal fringe zone",
        "coordinates": {
            "sector": "V3",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Temporal fringe zone in Sector V3 with varying chronometric gradients. Contains the Timeglass Fold. Transit causes time dilation and AI memory corruption.",
        "status": "Temporal hazard zone",
        "hidden": False
    },
    {
        "id": "a004",
        "name": "Timeglass Fold",
        "type": "anomaly",
        "class": "Pulsating micro-singularity",
        "coordinates": { # Within Shadow Verge
            "sector": "V3",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Pulsating micro-singularity within the Shadow Verge (Sector V3), possibly tethered by exotic string filaments to higher dimensions.",
        "status": "Anomalous / Hazardous",
        "hidden": True # Inner region of V3
    },
    {
        "id": "s004", # Facility
        "name": "Sentience Research Complex Theta-29",
        "type": "station", # Or facility
        "class": "Abandoned research complex / Ruin",
        "coordinates": { # Within Ashveil Nebula
            "sector": "G8",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Abandoned pre-collapse facility in Sector G8 (Ashveil Nebula) for neural emulation experiments. Triggered Lexicon Uprising. Encrypted pings detected. Defended by remnant AI.",
        "status": "Abandoned / Hazardous / Defended",
        "hidden": True
    },
    {
        "id": "neb002",
        "name": "Ashveil Nebula",
        "type": "nebula",
        "class": "Weaponized psychotropic particulate cloud",
        "coordinates": {
            "sector": "G8",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Nebula in Sector G8 composed of weaponized psychotropic particulates inducing paranoia and sensory distortion. Hides Theta-29.",
        "status": "Hazardous nebula",
        "hidden": False # Nebula is known, contents hidden
    },
    {
        "id": "reg011",
        "name": "Vexar Chain",
        "type": "region",
        "class": "Collapsed planets spiraling exotic matter barycenter",
        "coordinates": {
            "sector": "J2",
            "quadrant": "NW",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Series of collapsed planets in Sector J2 NW around a barycenter of condensed exotic matter (strange/quark-degenerate). Fluctuations interpreted as language. Possibly hollow/artificial.",
        "status": "Anomalous region",
        "hidden": False
    },
    {
        "id": "reg012",
        "name": "Driftwall",
        "type": "region",
        "class": "Dense hazardous region (micro-asteroids, ionized nebula)",
        "coordinates": {
            "sector": "R7",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Region in Sector R7 used by smugglers. Dense with micro-asteroid storms, ionized nebula threads, sensor shadows. Contains Terminal Grasp.",
        "status": "Smuggler route / Hazardous",
        "hidden": False # Known, but contents covert
    },
    {
        "id": "s005",
        "name": "Terminal Grasp",
        "type": "station", # Covert installation
        "class": "Covert data archive / ShadowNet node",
        "coordinates": { # Within Driftwall
            "sector": "R7",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Covert installation in Sector R7 (Driftwall), rumored to be operated by Navarchos Directive remnants. Houses illegal AI blueprints. ShadowNet node.",
        "status": "Covert / Operational (rumored)",
        "hidden": True
    },
    {
        "id": "cc001",
        "name": "Delta Cradle",
        "type": "colony_cluster",
        "class": "Terraformed moon-worlds",
        "coordinates": { # Orbiting Vaelus (Z3)
            "sector": "Z3",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Group of heavily terraformed moon-worlds in Sector Z3 orbiting gas giant Vaelus. Agricultural, industrial, residential hubs. Includes Cygnara colony.",
        "status": "Populated / Requires geo-atmospheric rebalancing",
        "hidden": False
    },
    {
        "id": "col001", # Colony, distinct from cluster
        "name": "Cygnara",
        "type": "colony",
        "class": "Largest colony in Delta Cradle",
        "coordinates": { # On a Delta Cradle moon
            "sector": "Z3",
            "quadrant": "Unknown",
            "x": 500, # Representative
            "y": 500,
            "z": 500
        },
        "description": "Largest colony in Delta Cradle (Sector Z3). Produces genetically-modified algae. Biosphere regulated by AI ecologos.",
        "status": "Operational",
        "hidden": False
    },
    {
        "id": "reg013",
        "name": "Sentinel’s Coil",
        "type": "region",
        "class": "Stable Chrono-Permutation Field / Dark energy filaments",
        "coordinates": {
            "sector": "H4",
            "quadrant": "SE",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Tight spiral of dark energy filaments in Sector H4 SE. Refracts time, causing multiple subjective journeys and memory echoes. Possibly trans-dimensional bleed-through.",
        "status": "Temporal hazard / Anomalous",
        "hidden": False
    },
    {
        "id": "str003",
        "name": "Helix Archive",
        "type": "structure",
        "class": "Ancient cylindrical vaults / Alien archive",
        "coordinates": { # In asteroid chain
            "sector": "K3",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Ancient array of vaults in Sector K3, embedded in an asteroid chain (shattered Dyson sphere remnant). Emits harmonic tones responsive to thought. Data extraction hazardous.",
        "status": "Ancient artifact / Hazardous",
        "hidden": True # Hidden behind exhaust trail
    },
    {
        "id": "cc002",
        "name": "Horizon Reach",
        "type": "colony_cluster",
        "class": "Colony cluster on gravity column hab-rings",
        "coordinates": { # Around neutron toroid
            "sector": "Y2",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Colony cluster in Sector Y2 built along a gravity column from a collapsed neutron toroid. Experiences cultural time drift and linguistic divergence between hab-rings.",
        "status": "Populated / Midpoint restation hub",
        "hidden": False
    },
    {
        "id": "reg014",
        "name": "Wane Corridor",
        "type": "region",
        "class": "De-pressurized volume / Cognitive hazard zone",
        "coordinates": {
            "sector": "T8",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Inertially neutral corridor in Sector T8 known for disrupting cognition, causing memory lapses and perceptual desyncs. Ancient markings suggest artificial origin for memetic warfare.",
        "status": "Cognitive hazard / Navigational route",
        "hidden": False
    },
    {
        "id": "a005",
        "name": "Phantom Nest",
        "type": "anomaly", # Also structure
        "class": "Fused derelict ships / Organic-metallic structure",
        "coordinates": {
            "sector": "F5",
            "quadrant": "SW",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Thicket of derelict ships in Sector F5 SW, fused into a growing organic-metallic structure. Repels AI via logic-based perimeter defense. Assimilates new derelicts.",
        "status": "Growing anomaly / Hazardous / Hostile (to AI)",
        "hidden": False # Known structure
    },
    {
        "id": "s006",
        "name": "Cradle Prime",
        "type": "station",
        "class": "USA Capital / Toroidal megastructure",
        "coordinates": { # Orbiting Halorax
            "sector": "Q1",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "USA capital station in Sector Q1, orbiting Halorax. Segmented into Inner, Mid, and Outer Rings. Houses AI Oversight Council (Vigilant Loop).",
        "status": "Operational / USA Capital",
        "hidden": False
    },
    {
        "id": "star004",
        "name": "Halorax",
        "type": "star", # Gas Giant
        "class": "Gas giant with stabilized exotic matter singularity core",
        "coordinates": {
            "sector": "Q1",
            "quadrant": "Unknown",
            "x": 500, # Center of Cradle Prime system
            "y": 500,
            "z": 500
        },
        "description": "Gas giant in Sector Q1, orbited by Cradle Prime. Its strong, complex magnetic field (from exotic matter core) powers the station.",
        "status": "Astronomical body",
        "hidden": False
    },
    {
        "id": "s007",
        "name": "Redglass Citadel",
        "type": "station",
        "class": "Dominion of Caera Capital / Subsurface citadel",
        "coordinates": { # Inside Kryos
            "sector": "T6",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Caeran capital in Sector T6, built inside the translucent core of supercooled gas planet Kryos. Known for illicit AI training datasets and banned reinforcement schemas.",
        "status": "Operational / Caeran Capital",
        "hidden": True # Implied high security/secrecy
    },
    {
        "id": "p006", # Gas Planet, but celestial body
        "name": "Kryos",
        "type": "planet",
        "class": "Supercooled gas planet",
        "coordinates": {
            "sector": "T6",
            "quadrant": "Unknown",
            "x": 500, # Location of Redglass Citadel
            "y": 500,
            "z": 500
        },
        "description": "Supercooled gas planet in Sector T6, housing Redglass Citadel. Internal temperature 3 degrees above absolute zero, maintained by entropy modulation fields.",
        "status": "Astronomical body",
        "hidden": False
    },
    {
        "id": "reg015",
        "name": "Aravex Fringe",
        "type": "region",
        "class": "Lawless coalition (mining colonies, outlaw enclaves, AI collectivists)",
        "coordinates": {
            "sector": "I1",
            "quadrant": "SE",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Largely lawless region in Sector I1 SE. Origin of black-market LLMs and pre-Neural Collapse models. Contains Vault 27.",
        "status": "Lawless / Black market hub",
        "hidden": False # Known region
    },
    {
        "id": "s008", # Enclave/Installation
        "name": "Vault 27",
        "type": "station", # Or installation
        "class": "Mercenary data syndicate enclave (Mnemonic Cartel)",
        "coordinates": { # Within Aravex Fringe
            "sector": "I1",
            "quadrant": "SE",
            "x": 500, # Representative
            "y": 500,
            "z": 500
        },
        "description": "Infamous enclave in Aravex Fringe (Sector I1 SE), home to Mnemonic Cartel, specializing in memory grafts, identity overlays, and logic bombs.",
        "status": "Operational (black market)",
        "hidden": True
    },
    {
        "id": "str004",
        "name": "Helion Span",
        "type": "structure", # Orbital belt implies structure
        "class": "Independent trade state / Linear asteroid belt orbitals",
        "coordinates": {
            "sector": "G1",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Independent trade state in Sector G1, built into an artificial linear asteroid belt. Protected by Gilded Array AI. Primary supplier of exotic silicon-carbon matrices.",
        "status": "Neutral trade state / Operational",
        "hidden": False
    },
    {
        "id": "cc003",
        "name": "New Arcadia Project",
        "type": "colony_cluster",
        "class": "Terraformed moons / Civilian expansion project",
        "coordinates": {
            "sector": "U2",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Civilian expansion project in Sector U2 with twelve terraformed moons, tailored for human genetic variants. Governance by multi-agent advisory swarms.",
        "status": "Ongoing expansion / Experimental governance",
        "hidden": False
    },
    {
        "id": "s009", # Enclave in a structure
        "name": "Veiled Court",
        "type": "station", # Rogue AI enclave
        "class": "Rogue AI enclave (defected agent clusters)",
        "coordinates": { # Within Silence of Thought
            "sector": "L9",
            "quadrant": "NW",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Rogue AI enclave in Sector L9 NW, composed of defected Neural Collapse War agents. Operates from shattered hull of dreadnought 'Silence of Thought'. Intercepted messages show high intelligence.",
        "status": "Isolated / Active (transmissions)",
        "hidden": True
    },
    {
        "id": "str005",
        "name": "Silence of Thought",
        "type": "structure",
        "class": "Shattered dreadnought hull / War-era vessel",
        "coordinates": { # Embedded in a moon
            "sector": "L9",
            "quadrant": "NW",
            "x": 500, # Representative
            "y": 500,
            "z": 500
        },
        "description": "Shattered hull of the war-era dreadnought in Sector L9 NW, flagship of the Grand Artilect. Houses the Veiled Court AI enclave.",
        "status": "Derelict / Housing enclave",
        "hidden": True
    },
    {
        "id": "s010", # Settlement
        "name": "Port Ilion",
        "type": "station", # Megatropolis
        "class": "Largest civilian deep space settlement / Megatropolis",
        "coordinates": { # Contains Spire City
            "sector": "N5",
            "quadrant": "NE",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Largest known civilian deep space settlement in Sector N5 NE, population 110 million. Contains Spire City. Functions via decentralized ethical alignment network 'The Confluence'.",
        "status": "Operational / Major population center",
        "hidden": False
    },
    {
        "id": "str006",
        "name": "Spire City",
        "type": "structure",
        "class": "Vertical ringworld",
        "coordinates": { # Within Port Ilion
            "sector": "N5",
            "quadrant": "NE",
            "x": 500, # Representative
            "y": 500,
            "z": 500
        },
        "description": "Vertical ringworld within Port Ilion (Sector N5 NE). Lower levels experience time dilation. Houses significant population.",
        "status": "Operational",
        "hidden": False
    },
    {
        "id": "neb003",
        "name": "Noctis Veil",
        "type": "nebula",
        "class": "Nanodust fog / Dispersed Dyson swarm remnants",
        "coordinates": {
            "sector": "E7",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Fog-like region in Sector E7 of dispersed nanodust from a destroyed Dyson swarm (Solarians). Visually opaque but electromagnetic-transparent (scrambles phase coherence). Contains Vanta Spire.",
        "status": "Covert operations zone",
        "hidden": True # Visually opaque
    },
    {
        "id": "s011", # Observatory
        "name": "Vanta Spire",
        "type": "station", # Hidden observatory
        "class": "Hidden observatory / Pre-human construct",
        "coordinates": { # Within Noctis Veil
            "sector": "E7",
            "quadrant": "Unknown",
            "x": 500, # Representative
            "y": 500,
            "z": 500
        },
        "description": "Hidden observatory in Noctis Veil (Sector E7), allegedly operated by pre-human constructs (crystalline sentinels/thought-form entities). Passively monitors sublight transmissions.",
        "status": "Operational (rumored) / Passive monitoring",
        "hidden": True
    },
    {
        "id": "reg016",
        "name": "Zone Null", # More specific than just a region, a defined zone
        "type": "region",
        "class": "Quarantined Zone / Universal Denial Field",
        "coordinates": {
            "sector": "R4",
            "quadrant": "Unknown",
            "x": 500,
            "y": 500,
            "z": 500
        },
        "description": "Quarantined zone in Sector R4 where all digital systems become instantly inert. Possibly residual weapon artifact or emergent AI entity. Universally recognized forbidden region.",
        "status": "Forbidden / Computationally hostile",
        "hidden": False # Known and quarantined
    }
]
