from vpython import *
from random import random, choice

scene.title = "AI Nuclear Plant - Smart Robot Inspection System v4"
scene.width = 1900
scene.height = 1000
scene.background = color.black
scene.forward = vector(-1, -0.3, -1)
scene.center = vector(0, 5, 0)
scene.range = 60

# SCENARIO PHASES
# Phase 0 : Normal Patrol           (0  - 80s)
# Phase 1 : Anomaly Detected        (80 - 110s)
# Phase 2 : Danger - Robot Retreats (110 - 140s)
# Phase 3 : Robot 2 Responds        (140 - 190s)
# Phase 4 : Suppression Active      (190 - 240s)
# Phase 5 : All Clear - Resume      (240s+)

scenario_phase = 0
scenario_timer = 0
phase_labels = [
    "PHASE 0 : NORMAL PATROL",
    "PHASE 1 : ANOMALY DETECTED",
    "PHASE 2 : DANGER CONFIRMED - ROBOT 1 RETREATING",
    "PHASE 3 : ROBOT 2 (SHIELDED) ENTERING ZONE C",
    "PHASE 4 : GAS SUPPRESSION ACTIVE",
    "PHASE 5 : ALL CLEAR - RESUMING PATROL",
]

# GROUND

ground = box(pos=vector(0,-0.5,0), size=vector(120,1,90), color=vector(0.3,0.3,0.3))

# FENCE

fc = color.yellow
for x in range(-55, 60, 10):
    box(pos=vector(x,1, 45), size=vector(0.5,3,0.5), color=fc)
    box(pos=vector(x,1,-45), size=vector(0.5,3,0.5), color=fc)
for z in range(-45, 50, 10):
    box(pos=vector( 55,1,z), size=vector(0.5,3,0.5), color=fc)
    box(pos=vector(-55,1,z), size=vector(0.5,3,0.5), color=fc)
box(pos=vector(0,2, 45),  size=vector(110,0.2,0.2), color=fc)
box(pos=vector(0,2,-45),  size=vector(110,0.2,0.2), color=fc)
box(pos=vector( 55,2,0),  size=vector(0.2,0.2,90),  color=fc)
box(pos=vector(-55,2,0),  size=vector(0.2,0.2,90),  color=fc)

# ZONE MARKERS

box(pos=vector(-25,-0.4,-5), size=vector(15,0.1,15), color=vector(0.5,0,0),   opacity=0.5)
label(pos=vector(-25,0.2,5),  text="ZONE A\nREACTOR",  color=color.red,    box=False, height=13)

box(pos=vector(-5,-0.4,10),  size=vector(18,0.1,14), color=vector(0.5,0.5,0), opacity=0.5)
label(pos=vector(-5,0.2,17), text="ZONE B\nTURBINE",  color=color.yellow, box=False, height=13)

box(pos=vector(5,-0.4,-15),  size=vector(14,0.1,14), color=vector(0,0,0.5),   opacity=0.5)
label(pos=vector(5,0.2,-8),  text="ZONE C\nPUMP",     color=color.cyan,   box=False, height=13)

box(pos=vector(25,-0.4,0),   size=vector(18,0.1,18), color=vector(0,0.4,0),   opacity=0.5)
label(pos=vector(25,0.2,10), text="ZONE D\nCOOLING",  color=color.green,  box=False, height=13)

# SPECIAL ZONES

# Control Room - NO ENTRY zone (red boundary)
box(pos=vector(-42,0,-0.4,20), size=vector(12,0.1,10), color=color.red, opacity=0.4) if False else None
box(pos=vector(-42,-0.4,20),   size=vector(14,0.1,12), color=color.red, opacity=0.4)
label(pos=vector(-42,1,20), text="NO ENTRY\nCONTROL ROOM", color=color.red, box=False, height=12)

# Zone D patrol path marker (robot goes AROUND this)
box(pos=vector(25,-0.45,0), size=vector(20,0.05,20), color=color.green, opacity=0.2)
label(pos=vector(25,0.3,-12), text="ZONE D: ROBOT GOES AROUND", color=color.green, box=False, height=11)

# Pump station inspect marker
box(pos=vector(5,-0.45,-15), size=vector(10,0.05,10), color=color.cyan, opacity=0.3)
label(pos=vector(5,0.3,-20), text="PUMP: ROBOT STOPS & INSPECTS", color=color.cyan, box=False, height=11)

# Safe zone for Robot 1
box(pos=vector(-50,0.1,30), size=vector(8,0.2,8), color=color.blue, opacity=0.5)
label(pos=vector(-50,1,30), text="SAFE ZONE\nROBOT RETREAT", color=color.blue, box=False, height=12)

# Assembly point
box(pos=vector(-50,0.1,-35), size=vector(10,0.2,8), color=color.green, opacity=0.7)
label(pos=vector(-50,1,-35), text="ASSEMBLY POINT", box=False, color=color.green, height=13)

# Charging station (robot base)
box(pos=vector(-48,-0.4,10), size=vector(5,0.1,5), color=color.magenta, opacity=0.5)
label(pos=vector(-48,0.5,10), text="CHARGING BASE", color=color.magenta, box=False, height=12)

# BUILDINGS

cylinder(pos=vector(-25,0,-5), axis=vector(0,8,0), radius=5, color=color.red)
sphere(pos=vector(-25,8,-5), radius=5, color=color.orange)
label(pos=vector(-25,15,-5), text="NUCLEAR REACTOR", box=False, height=20, color=color.red)

box(pos=vector(-5,4,10),   size=vector(15,8,10), color=color.white)
label(pos=vector(-5,10,10), text="TURBINE HALL",   box=False)

box(pos=vector(5,3,-15),   size=vector(10,6,10), color=color.white)
label(pos=vector(5,10,-15), text="PUMP STATION",   box=False)

cylinder(pos=vector(25,0,0),  axis=vector(0,4,0),  radius=7, color=color.gray(0.7), opacity=0.35)
cylinder(pos=vector(25,4,0),  axis=vector(0,6,0),  radius=4, color=color.gray(0.8), opacity=0.35)
cylinder(pos=vector(25,10,0), axis=vector(0,7,0),  radius=8, color=color.gray(0.9), opacity=0.35)
label(pos=vector(25,20,0), text="COOLING TOWER", box=False, height=18)

box(pos=vector(-42,3,20), size=vector(12,6,10), color=vector(0.2,0.2,0.6))
label(pos=vector(-42,8,20), text="CONTROL ROOM",  box=False, color=color.cyan, height=16)
for wz in [-3,0,3]:
    box(pos=vector(-36,4,20+wz), size=vector(0.1,2,1.5), color=color.cyan, opacity=0.6)

box(pos=vector(40,3,-25), size=vector(12,6,10), color=vector(0.3,0.5,0.1))
label(pos=vector(40,8,-25), text="WASTE STORAGE", box=False, color=color.green, height=16)

# PIPES

cylinder(pos=vector(-10,2,0),  axis=vector(35,0,0),  radius=0.6, color=color.cyan)
cylinder(pos=vector(5,2,-10),  axis=vector(0,0,-15), radius=0.5, color=color.cyan)
cylinder(pos=vector(-25,2,-5), axis=vector(30,0,0),  radius=0.5, color=color.cyan)
cylinder(pos=vector(25,2,-5),  axis=vector(0,0,5),   radius=0.5, color=color.cyan)

# WATER BUBBLES STEAM

water = cylinder(pos=vector(25,0.1,0), axis=vector(0,1.5,0), radius=6, color=color.cyan, opacity=0.7)
bubbles = []
for i in range(25):
    b = sphere(pos=vector(25+random()*4-2, 0.2, random()*4-2), radius=0.35, color=color.white, opacity=0.5)
    bubbles.append(b)
steam = []
for i in range(40):
    s = sphere(pos=vector(25+random()*2-1, 16+random()*3, random()*2-1), radius=0.4, color=color.white, opacity=0.3)
    steam.append(s)

# WARNING LIGHTS

warn_a = sphere(pos=vector(-25,14,-5), radius=0.7, color=color.red,    emissive=True, visible=False)
warn_c = sphere(pos=vector(5,7,-15),   radius=0.7, color=color.orange, emissive=True, visible=False)

# GAS CLOUD & FIRE

gas_cloud = []
for i in range(35):
    g = sphere(pos=vector(5+random()*5-2.5, 0.5+random()*4, -15+random()*5-2.5),
               radius=0.65, color=color.green, opacity=0.0)
    gas_cloud.append(g)

fire_particles = []
for i in range(20):
    f = sphere(pos=vector(5+random()*3-1.5, 0.5+random()*3, -15+random()*3-1.5),
               radius=0.35, color=color.red, opacity=0.0)
    fire_particles.append(f)

# SPRAY PARTICLES

spray_particles = []
for i in range(25):
    sp = sphere(pos=vector(5,2,-15), radius=0.25, color=color.white, opacity=0.0)
    spray_particles.append(sp)
spray_angle = 0

# WIRELESS SIGNAL RINGS (Robot <-> Drone comms)
# Expanding rings from robot show wireless broadcast

# Signal rings around robot (expand outward = transmitting)
signal_rings = []
for i in range(4):
    sr = ring(pos=vector(-48,1.5,10),
              axis=vector(0,1,0),
              radius=0.1 + i*0.5,
              thickness=0.06,
              color=color.cyan,
              opacity=0.0)
    signal_rings.append(sr)

# Signal rings around drone (receiving)
drone_rings = []
for i in range(3):
    dr = ring(pos=vector(0,18,0),
              axis=vector(0,1,0),
              radius=0.1 + i*0.4,
              thickness=0.05,
              color=color.yellow,
              opacity=0.0)
    drone_rings.append(dr)

signal_ring_timer  = 0.0
signal_ring_phase  = [i * 0.4 for i in range(4)]   # stagger each ring
drone_ring_phase   = [i * 0.35 for i in range(3)]

# Shared synced data (what both robot & drone see after sync)
synced_data = {"gas": 0.5, "temp": 30.0, "rad": 5.0, "pressure": 101.0}
sync_delay_counter = 0   # counts up when signal weak

# WORKERS

workers = []
w_starts  = [vector(-5,1,10), vector(5,1,-12), vector(-20,1,0), vector(0,1,5)]
w_targets = [vector(-50,1,-35)] * 4
for wp in w_starts:
    wb = sphere(pos=vector(wp.x,wp.y,wp.z),             radius=0.5, color=color.white)
    wl = sphere(pos=vector(wp.x,wp.y+0.7,wp.z),         radius=0.3, color=color.yellow)
    workers.append([wb, wl])

# ROBOT 1 — Patrol with Rules
# Patrol order:
#   Start -> Zone A -> Zone B -> PUMP(inspect) ->
#   Around Zone D (not through) -> back
#   NEVER goes near Control Room

# Waypoints carefully placed to:
# - go AROUND Zone D (waypoints circle it)
# - STOP at Pump Station (Zone C)
# - NEVER enter Control Room area (x<-36, z>14)
wp_patrol = [
    vector(-48, 1, 10),   # 0: Charging base (start)
    vector(-25, 1, 0),    # 1: Zone A - Reactor
    vector(-5,  1, 10),   # 2: Zone B - Turbine
    vector(5,   1, -15),  # 3: Zone C - PUMP (inspect here - robot pauses)
    vector(15,  1, -20),  # 4: South of Zone D
    vector(35,  1, -10),  # 5: East of Zone D (going around)
    vector(38,  1,  5),   # 6: East side of Zone D
    vector(35,  1, 15),   # 7: North of Zone D (completed loop around)
    vector(15,  1, 10),   # 8: Back inside
    vector(-10, 1,  0),   # 9: Middle corridor (away from Control Room)
    vector(-48, 1, 10),   # 10: Back to charging base
]

PUMP_INSPECT_WP   = 3     # waypoint index where robot stops to inspect
INSPECT_DURATION  = 8.0   # seconds robot pauses at pump station
wp_index          = 0
inspect_timer     = 0.0
is_inspecting     = False

r1_safe_pos   = vector(-50, 1, 30)
r1_retreated  = False

robot_body   = box(pos=vector(-48,1,10),          size=vector(3,1.5,2),  color=color.orange)
robot_head   = sphere(pos=vector(-48,2.2,10),     radius=0.6,            color=color.white)
wheel1       = cylinder(pos=vector(-49.2,0.5,11), axis=vector(0,0,-2),   radius=0.5, color=color.black)
wheel2       = cylinder(pos=vector(-46.8,0.5,11), axis=vector(0,0,-2),   radius=0.5, color=color.black)
robot_arm    = cylinder(pos=robot_body.pos+vector(1.5,0.5,0),
                        axis=vector(2,0,0), radius=0.2, color=color.gray(0.6))
robot_light  = sphere(pos=robot_body.pos+vector(0,1.2,0),
                      radius=0.35, color=color.green, emissive=True)
robot_beacon = sphere(pos=robot_body.pos+vector(0,1.8,0),
                      radius=0.3,  color=color.red,   emissive=True, visible=False)
robot1_label = label(pos=robot_body.pos+vector(0,3.2,0),
                     text="🤖 R1-INSPECTOR", height=12,
                     color=color.orange, box=False, opacity=0)

signal_ring  = ring(pos=robot_body.pos+vector(0,1.5,0),
                    axis=vector(0,1,0), radius=1.0, thickness=0.15,
                    color=color.yellow, visible=False)
signal_scale  = 1.0
signal_growing = True

# ROBOT 2 — Shielded Responder

robot2_body   = box(pos=vector(-55,1,-35),          size=vector(3.5,2,2.5), color=vector(0.6,0,0), visible=False)
robot2_head   = sphere(pos=vector(-55,2.5,-35),     radius=0.7,             color=color.gray(0.8), visible=False)
robot2_w1     = cylinder(pos=vector(-56.5,0.5,-34), axis=vector(0,0,-2.5),  radius=0.55, color=color.black, visible=False)
robot2_w2     = cylinder(pos=vector(-53.5,0.5,-34), axis=vector(0,0,-2.5),  radius=0.55, color=color.black, visible=False)
robot2_light  = sphere(pos=vector(-55,3,-35),       radius=0.4,             color=color.red, emissive=True, visible=False)
robot2_shield = box(pos=vector(-55,1.5,-35),        size=vector(5,3,4),     color=color.cyan, opacity=0.15, visible=False)
robot2_arm    = cylinder(pos=vector(-55,1.5,-35),   axis=vector(3,0,0),     radius=0.25, color=color.cyan, visible=False)
robot2_label  = label(pos=vector(-55,4.5,-35),
                      text="🛡 R2-RESPONDER", height=12,
                      color=color.red, box=False, opacity=0, visible=False)
r2_target     = vector(5,1,-15)
r2_arrived    = False

# DRONE

drone_body = sphere(pos=vector(0,18,0),   radius=1,                color=color.blue)
drone_label= label(pos=vector(0,20.5,0),
                   text="✈ DRONE-1", height=12,
                   color=color.cyan, box=False, opacity=0)
drone_arm1 = box(pos=vector(0,18,0),      size=vector(5,0.2,0.2),  color=color.white)
drone_arm2 = box(pos=vector(0,18,0),      size=vector(0.2,0.2,5),  color=color.white)
rotor1 = box(pos=vector( 2.5,18.2,0),    size=vector(1.5,0.1,0.3), color=color.cyan)
rotor2 = box(pos=vector(-2.5,18.2,0),    size=vector(1.5,0.1,0.3), color=color.cyan)
rotor3 = box(pos=vector(0,18.2, 2.5),    size=vector(0.3,0.1,1.5), color=color.cyan)
rotor4 = box(pos=vector(0,18.2,-2.5),    size=vector(0.3,0.1,1.5), color=color.cyan)
drone_angle  = 0
drone_radius = 30
rotor_angle  = 0

# CONTAINMENT BOX

containment = box(pos=vector(5,2,-15), size=vector(12,4,12), color=color.yellow, opacity=0.0)

# BATTERY SYSTEM

robot_battery = 100.0    # %
drone_battery = 100.0    # %

# drain rates per second
ROBOT_DRAIN   = 0.04     # robot drains slower
DRONE_DRAIN   = 0.06     # drone drains faster (flying costs more)

ROBOT_LOW_THRESHOLD = 20.0
DRONE_LOW_THRESHOLD = 25.0

robot_battery_low = False
drone_battery_low = False

# DASHBOARD PANELS

phase_panel    = label(pixel_pos=True, pos=vector(960,960,0),  box=True, border=12,
                       background=color.black, color=color.cyan, height=19)
robot_panel    = label(pixel_pos=True, pos=vector(190,720,0),  box=True, border=10,
                       background=color.black, color=color.orange)
robot2_panel   = label(pixel_pos=True, pos=vector(190,530,0),  box=True, border=10,
                       background=color.black, color=color.red)
drone_panel    = label(pixel_pos=True, pos=vector(190,360,0),  box=True, border=10,
                       background=color.black, color=color.cyan)
alarm_panel    = label(pixel_pos=True, pos=vector(190,170,0),  box=True, border=10,
                       background=color.green, color=color.white, height=17)
connect_panel  = label(pixel_pos=True, pos=vector(1660,700,0), box=True, border=10,
                       background=color.black, color=color.yellow)
zone_panel     = label(pixel_pos=True, pos=vector(1660,470,0), box=True, border=10,
                       background=color.black, color=color.white)
action_log     = label(pixel_pos=True, pos=vector(1660,230,0), box=True, border=10,
                       background=color.black, color=color.green, height=13)

# GRAPHS

scene.append_to_caption("\n\nNUCLEAR PLANT LIVE MONITORING\n\n")

temp_graph  = graph(title="Temperature", xtitle="Time", ytitle="Temp (C)",    width=870, height=165)
temp_curve  = gcurve(color=color.orange, label="Temperature")
temp_limit  = gcurve(color=color.white,  label="Limit 42C")

rad_graph   = graph(title="Radiation",   xtitle="Time", ytitle="Rad (mSv)",   width=870, height=165)
rad_curve   = gcurve(color=color.red,    label="Radiation")
rad_limit   = gcurve(color=color.white,  label="Safe Limit 10")

gas_graph   = graph(title="Gas Level",   xtitle="Time", ytitle="Gas (ppm)",   width=870, height=165)
gas_curve   = gcurve(color=color.green,  label="Gas Level")
gas_limit   = gcurve(color=color.white,  label="Safe Limit 3")

batt_graph  = graph(title="Battery Levels", xtitle="Time", ytitle="Battery %", width=870, height=165)
batt_robot  = gcurve(color=color.orange, label="Robot Battery")
batt_drone  = gcurve(color=color.cyan,   label="Drone Battery")
batt_low    = gcurve(color=color.red,    label="Low Battery Line")

alert_graph = graph(title="Alert Level", xtitle="Time", ytitle="Level (0-3)", width=870, height=165)
alert_curve = gcurve(color=color.yellow, label="Alert Level")

# STATE VARIABLES

time_counter    = 0
temperature     = 30.0
pressure        = 101.0
radiation       = 5.0
gas             = 0.5
alert_level     = 0
reaction_timer  = 0
sensor_timer    = 0
update_interval = 1.5

alert_names  = ["ALL CLEAR", "CAUTION", "WARNING", "EMERGENCY"]
alert_colors = [color.green, color.yellow, color.orange, color.red]

flash_timer  = 0
log_lines    = ["System boot complete.", "All sensors online.", "Robot 1 patrol started."]

def add_log(msg):
    log_lines.append(msg)
    if len(log_lines) > 9:
        log_lines.pop(0)

def get_zone(pos):
    x, z = pos.x, pos.z
    if -33<x<-17 and -12<z<2:  return "A"
    if -13<x<4   and  5<z<17:  return "B"
    if  -1<x<12  and -22<z<-8: return "C"
    if  16<x<34  and  -9<z<9:  return "D"
    return "TRANSIT"

def move_toward(pos, target, spd):
    diff = target - pos
    if mag(diff) < 0.4:
        return pos, True
    return pos + norm(diff) * spd, False

def update_robot1(new_pos):
    robot_body.pos   = new_pos
    robot_head.pos   = new_pos + vector(0, 1.2, 0)
    wheel1.pos       = new_pos + vector(-1.2,-0.5, 1)
    wheel2.pos       = new_pos + vector( 1.2,-0.5, 1)
    robot_arm.pos    = new_pos + vector(1.5, 0.5, 0)
    robot_light.pos  = new_pos + vector(0, 1.2, 0)
    robot_beacon.pos = new_pos + vector(0, 1.8, 0)
    signal_ring.pos  = new_pos + vector(0, 1.5, 0)
    robot1_label.pos = new_pos + vector(0, 3.2, 0)

def update_robot2(new_pos):
    robot2_body.pos   = new_pos
    robot2_head.pos   = new_pos + vector(0, 1.5, 0)
    robot2_w1.pos     = new_pos + vector(-1.5,-0.5, 1)
    robot2_w2.pos     = new_pos + vector( 1.5,-0.5, 1)
    robot2_light.pos  = new_pos + vector(0, 2, 0)
    robot2_shield.pos = new_pos + vector(0, 0.5, 0)
    robot2_arm.pos    = new_pos + vector(1.5, 0.5, 0)
    robot2_label.pos  = new_pos + vector(0, 4.5, 0)

def battery_color(pct):
    if pct > 50: return color.green
    if pct > 20: return color.yellow
    return color.red

# MAIN LOOP

while True:

    rate(40)

    dt = 1/40
    scenario_timer += dt
    flash_timer    += dt
    rotor_angle    += 0.15
    spray_angle    += 0.08

    # BATTERY DRAIN
    robot_battery = max(0, robot_battery - ROBOT_DRAIN * dt)
    drone_battery = max(0, drone_battery - DRONE_DRAIN * dt)

    robot_battery_low = robot_battery < ROBOT_LOW_THRESHOLD
    drone_battery_low = drone_battery < DRONE_LOW_THRESHOLD

    if robot_battery_low and "Robot battery LOW" not in " ".join(log_lines):
        add_log("!!! Robot 1 battery LOW: " + str(round(robot_battery,1)) + "%")
    if drone_battery_low and "Drone battery LOW" not in " ".join(log_lines):
        add_log("!!! Drone battery LOW: " + str(round(drone_battery,1)) + "%")

    # PHASE TRANSITIONS

    if scenario_timer >= 80  and scenario_phase == 0:
        scenario_phase = 1
        add_log("ANOMALY: Gas rising at Zone C (Pump)")
        add_log("Robot 1 moving to investigate edge...")

    if scenario_timer >= 110 and scenario_phase == 1:
        scenario_phase = 2
        add_log("GAS LEAK CONFIRMED! Danger level HIGH")
        add_log("Robot 1 RETREATING to safe zone!")
        robot_body.color = color.yellow

    if scenario_timer >= 140 and scenario_phase == 2:
        scenario_phase = 3
        add_log("Robot 1 safe. Broadcasting alert signal.")
        add_log("Robot 2 (SHIELDED) deployed to Zone C!")
        for obj in [robot2_body, robot2_head, robot2_w1, robot2_w2,
                    robot2_light, robot2_shield, robot2_arm, robot2_label]:
            obj.visible = True

    if scenario_timer >= 190 and scenario_phase == 3:
        scenario_phase = 4
        add_log("Robot 2 at Zone C. Spray arm ACTIVE.")
        add_log("Gas suppression in progress...")

    if scenario_timer >= 240 and scenario_phase == 4:
        scenario_phase = 5
        add_log("Gas sealed. Robot 2 signals ALL CLEAR.")
        add_log("Robot 1 resuming normal patrol!")
        robot_body.color     = color.orange
        robot_beacon.visible = False
        signal_ring.visible  = False
        wp_index = 0

    # ROBOT 1 MOVEMENT + PATROL RULES

    current_zone = get_zone(robot_body.pos)

    if scenario_phase == 0 or scenario_phase == 5:

        target_wp = wp_patrol[wp_index % len(wp_patrol)]

        # PUMP STATION: pause and inspect
        if (wp_index % len(wp_patrol)) == PUMP_INSPECT_WP:
            new_pos, reached = move_toward(robot_body.pos, target_wp, 0.07)
            update_robot1(new_pos)
            if reached:
                if not is_inspecting:
                    is_inspecting = True
                    inspect_timer = 0.0
                    robot_arm.axis = vector(4, 0, 0)   # arm out scanning
                    add_log("Robot 1 stopped at Pump. Inspecting...")
                else:
                    inspect_timer += dt
                    # Rotate arm slowly while inspecting
                    robot_arm.axis = vector(
                        3.5*cos(inspect_timer*1.2),
                        0,
                        3.5*sin(inspect_timer*1.2)
                    )
                    if inspect_timer >= INSPECT_DURATION:
                        is_inspecting = False
                        robot_arm.axis = vector(2, 0, 0)
                        wp_index = (wp_index + 1) % len(wp_patrol)
                        add_log("Pump inspection done. Continuing patrol.")
        else:
            is_inspecting = False
            spd = 0.07 if not robot_battery_low else 0.04   # slow if battery low
            new_pos, reached = move_toward(robot_body.pos, target_wp, spd)
            update_robot1(new_pos)
            robot_arm.axis = vector(2, 0, 0)
            if reached:
                wp_index = (wp_index + 1) % len(wp_patrol)

        robot_light.color = battery_color(robot_battery)

    elif scenario_phase == 1:
        # Investigate - move to edge of Zone C (not inside)
        investigate_pos = vector(12, 1, -12)
        new_pos, _ = move_toward(robot_body.pos, investigate_pos, 0.07)
        update_robot1(new_pos)
        robot_arm.axis    = vector(3.5, 0, 0)
        robot_light.color = color.yellow
        robot_beacon.visible = True

    elif scenario_phase == 2:
        # RETREAT away from danger to safe corner
        new_pos, reached = move_toward(robot_body.pos, r1_safe_pos, 0.13)
        update_robot1(new_pos)
        robot_arm.axis    = vector(2, 0, 0)
        robot_light.color = color.red
        robot_beacon.visible = True
        if reached:
            r1_retreated = True

    elif scenario_phase == 3 or scenario_phase == 4:
        # Stay at safe zone, pulse signal ring
        update_robot1(r1_safe_pos)
        robot_arm.axis       = vector(2, 0, 0)
        robot_light.color    = color.red
        robot_beacon.visible = True
        signal_ring.visible  = True

    # Signal ring pulse
    if signal_ring.visible:
        if signal_growing:
            signal_scale += 0.05
            signal_ring.radius = signal_scale
            if signal_scale > 4.0: signal_growing = False
        else:
            signal_scale -= 0.05
            signal_ring.radius = signal_scale
            if signal_scale < 1.0: signal_growing = True

    # ROBOT 2

    if scenario_phase >= 3:
        if not r2_arrived:
            new_pos2, r2_arrived = move_toward(robot2_body.pos, r2_target, 0.14)
            update_robot2(new_pos2)
        else:
            update_robot2(r2_target)
        if scenario_phase >= 4:
            robot2_arm.axis    = vector(4, 0, 0)
            robot2_light.color = color.white   # white = spray active
        else:
            robot2_arm.axis    = vector(2, 0, 0)
            robot2_light.color = color.red

    # DISTANCE: Robot <-> Drone

    robot_drone_dist = mag(drone_body.pos - robot_body.pos)
    conn_status_str  = "STRONG" if robot_drone_dist < 30 else ("WEAK" if robot_drone_dist < 45 else "LOST")

    # WIRELESS SIGNAL ANIMATION
    # Rings expand outward from robot & drone

    signal_ring_timer += dt

    # Robot transmit rings - expand and fade out
    for i, sr in enumerate(signal_rings):
        phase = (signal_ring_timer + signal_ring_phase[i]) % 1.2
        sr.pos     = robot_body.pos + vector(0, 1.5, 0)
        sr.radius  = 0.5 + phase * 4.0          # expand from 0.5 to 5.3
        sr.opacity = max(0, 0.7 - phase * 0.6)  # fade as it expands
        # color based on signal strength
        if conn_status_str == "STRONG":
            sr.color = color.cyan
        elif conn_status_str == "WEAK":
            sr.color = color.yellow
        else:
            sr.color = color.red

    # Drone receive rings - smaller, yellow
    for i, dr in enumerate(drone_rings):
        phase = (signal_ring_timer + drone_ring_phase[i]) % 1.0
        dr.pos     = drone_body.pos + vector(0, 0.5, 0)
        dr.radius  = 0.3 + phase * 2.5
        dr.opacity = max(0, 0.5 - phase * 0.5)
        dr.color   = color.cyan if conn_status_str == "STRONG" else (color.yellow if conn_status_str == "WEAK" else color.red)

    # Sync delay: if signal weak/lost, data updates slower
    sync_delay_counter += 1
    sync_interval = 1 if conn_status_str == "STRONG" else (3 if conn_status_str == "WEAK" else 8)
    if sync_delay_counter >= sync_interval:
        sync_delay_counter = 0
        synced_data["gas"]      = gas
        synced_data["temp"]     = temperature
        synced_data["rad"]      = radiation
        synced_data["pressure"] = pressure

    # DRONE

    drone_angle += 0.01 if scenario_phase <= 1 else 0.025
    if scenario_phase >= 2:
        dtarget = vector(5, 10, -15)
    else:
        # Drone loosely follows robot horizontally + stays high
        follow_x = robot_body.pos.x * 0.3 + drone_radius * sin(drone_angle) * 0.7
        follow_z = robot_body.pos.z * 0.3 + drone_radius * cos(drone_angle) * 0.7
        dtarget   = vector(follow_x, 18, follow_z)

    drone_body.pos += (dtarget - drone_body.pos) * 0.02
    drone_label.pos = drone_body.pos + vector(0, 2.5, 0)
    drone_arm1.pos  = drone_body.pos
    drone_arm2.pos  = drone_body.pos

    r_offs = [vector(2.5,0.2,0),vector(-2.5,0.2,0),vector(0,0.2,2.5),vector(0,0.2,-2.5)]
    for r, off in zip([rotor1,rotor2,rotor3,rotor4], r_offs):
        r.pos = drone_body.pos + off
    rotor1.axis = vector(1.5*cos(rotor_angle),      0.1, 1.5*sin(rotor_angle))
    rotor2.axis = vector(1.5*cos(rotor_angle+pi),   0.1, 1.5*sin(rotor_angle+pi))
    rotor3.axis = vector(1.5*cos(rotor_angle+pi/2), 0.1, 1.5*sin(rotor_angle+pi/2))
    rotor4.axis = vector(1.5*cos(rotor_angle-pi/2), 0.1, 1.5*sin(rotor_angle-pi/2))

    # SPRAY, GAS CLOUD, FIRE

    if scenario_phase == 4:
        for i, sp in enumerate(spray_particles):
            angle_i = spray_angle + i*(2*pi/len(spray_particles))
            sp.color   = color.white
            sp.opacity = 0.3 + random()*0.5   # flickering mist effect
            sp.radius  = 0.2 + random()*0.25  # particles vary in size
            sp.pos = vector(
                r2_target.x + 2 + random()*3,
                r2_target.y + random()*2.5,
                r2_target.z + sin(angle_i)*1.5
            )
    else:
        for sp in spray_particles:
            sp.opacity = 0.0

    if scenario_phase >= 1:
        grow = min(0.55, (scenario_timer-80)/60.0)
        if scenario_phase >= 4:
            grow = max(0, grow - (scenario_timer-190)*0.005)
        for g in gas_cloud:
            g.opacity = grow
            g.pos.y  += 0.03
            g.pos.x  += (random()-0.5)*0.04
            if g.pos.y > 6: g.pos.y = 0.5
    else:
        for g in gas_cloud: g.opacity = 0

    if scenario_phase == 3:
        for f in fire_particles:
            f.opacity = 0.8
            f.color   = choice([color.red, color.orange, color.yellow])
            f.pos.y  += 0.08
            if f.pos.y > 5: f.pos.y = 0.5
    else:
        for f in fire_particles: f.opacity = 0.0

    if scenario_phase >= 5 and containment.opacity < 0.3:
        containment.opacity += 0.001

    # WORKERS

    if scenario_phase >= 2:
        for i, (wb, wl) in enumerate(workers):
            dw = w_targets[i] - wb.pos
            if mag(dw) > 0.5:
                wb.pos += norm(dw) * 0.1
                wl.pos  = wb.pos + vector(0,0.7,0)

    # WARNING LIGHTS

    if flash_timer > 0.4:
        flash_timer = 0
        if scenario_phase >= 1:
            warn_a.visible = not warn_a.visible
            warn_c.visible = not warn_c.visible

    # STEAM & BUBBLES

    for s in steam:
        s.pos.y += 0.05
        if s.pos.y > 28: s.pos.y = 16
    for b in bubbles:
        b.pos.y += 0.05
        if b.pos.y > 2: b.pos.y = 0.2

    # SENSOR + DASHBOARD UPDATE

    sensor_timer += dt
    if sensor_timer > update_interval:
        sensor_timer   = 0
        reaction_timer += 1
        time_counter   += 1

        if scenario_phase == 0:
            temperature = 30 + random()*3;  pressure = 101 + random()*2
            radiation   = 4  + random()*2;  gas      = 0.3 + random()*0.4
            alert_level = 0
        elif scenario_phase == 1:
            temperature = 34 + random()*4;  pressure = 103 + random()*3
            radiation   = 6  + random()*3;  gas      = 2.5 + random()*1.2
            alert_level = 1
        elif scenario_phase == 2:
            temperature = 40 + random()*5;  pressure = 107 + random()*4
            radiation   = 9  + random()*4;  gas      = 5   + random()*2
            alert_level = 2
        elif scenario_phase == 3:
            temperature = 47 + random()*8;  pressure = 112 + random()*5
            radiation   = 13 + random()*4;  gas      = 7   + random()*2
            alert_level = 3
        elif scenario_phase == 4:
            temperature = max(35, temperature - 0.8 + random()*0.3)
            pressure    = max(103, pressure   - 0.5 + random()*0.3)
            radiation   = max(6,   radiation  - 0.6 + random()*0.3)
            gas         = max(1.5, gas        - 0.9 + random()*0.3)
            alert_level = 2
        elif scenario_phase == 5:
            temperature = max(30, temperature - 0.4 + random()*0.2)
            pressure    = max(101, pressure   - 0.3 + random()*0.2)
            radiation   = max(4,   radiation  - 0.3 + random()*0.2)
            gas         = max(0.3, gas        - 0.4 + random()*0.1)
            alert_level = 0 if gas < 1.0 else 1

        # Update floating name label colors based on alert
        robot1_label.color = alert_colors[alert_level]
        robot1_label.text  = ("🤖 R1-INSPECTOR  [" + ("RETREATED" if scenario_phase in [2,3,4] else "PATROLLING") + "]")
        drone_label.color  = alert_colors[alert_level]
        drone_label.text   = ("✈ DRONE-1  [" + ("SCANNING LEAK" if scenario_phase >= 2 else "AERIAL PATROL") + "]")
        if scenario_phase >= 3:
            robot2_label.color = color.red if scenario_phase == 3 else color.cyan
            robot2_label.text  = ("🛡 R2-RESPONDER  [" + ("MOVING" if scenario_phase == 3 else "SUPPRESSING") + "]")
        r1_mode = ["NORMAL PATROL","INVESTIGATING ZONE C","RETREATING TO SAFE ZONE",
                   "AT SAFE ZONE - ALERTING","AT SAFE ZONE - MONITORING","RESUMING PATROL"][scenario_phase]
        r1_inspect_txt = ("INSPECTING (" + str(round(inspect_timer,1)) + "/" + str(INSPECT_DURATION) + "s)" if is_inspecting else "MOVING")

        robot_panel.text = (
            "ROBOT 1  (PATROL / DETECTOR)\n\n"
            "Status    : " + r1_mode + "\n"
            "Zone      : " + current_zone + "\n"
            "Position  : (" + str(round(robot_body.pos.x,1)) + ", " + str(round(robot_body.pos.z,1)) + ")\n"
            "Pump Stop : " + r1_inspect_txt + "\n"
            "Battery   : " + str(round(robot_battery,1)) + "% " + ("!!! LOW !!!" if robot_battery_low else "OK") + "\n"
            "Arm       : " + ("SCANNING" if robot_arm.axis.x > 3 or robot_arm.axis.z != 0 else "RETRACTED")
        )

        r2_mode = ["STANDBY","STANDBY","STANDBY","MOVING TO ZONE C","SUPPRESSING GAS","SEALED - DONE"][scenario_phase]
        robot2_panel.text = (
            "ROBOT 2  (SHIELDED RESPONDER)\n\n"
            "Status    : " + r2_mode + "\n"
            "Shield    : " + ("ACTIVE" if scenario_phase >= 3 else "OFF") + "\n"
            "Spray Arm : " + ("ACTIVE" if scenario_phase == 4 else "OFF") + "\n"
            "Position  : (" + str(round(robot2_body.pos.x,1)) + ", " + str(round(robot2_body.pos.z,1)) + ")"
        )

        conn_status = "STRONG" if robot_drone_dist < 30 else ("WEAK" if robot_drone_dist < 45 else "LOST")
        drone_panel.text = (
            "DRONE  (AERIAL MONITOR)\n\n"
            "Battery   : " + str(round(drone_battery,1)) + "% " + ("!!! LOW !!!" if drone_battery_low else "OK") + "\n"
            "Altitude  : " + str(round(drone_body.pos.y,1)) + " m\n"
            "Temp      : " + str(round(synced_data["temp"],2)) + " C\n"
            "Gas       : " + str(round(synced_data["gas"],2)) + " ppm\n"
            "Mode      : " + ("SCANNING LEAK SITE" if scenario_phase >= 2 else "AERIAL PATROL")
        )

        connect_panel.text = (
            "WIRELESS COMMS  [Robot <-> Drone]\n\n"
            "Signal Strength : " + conn_status + "\n"
            "Distance        : " + str(round(robot_drone_dist,1)) + " m\n"
            "Sync Status     : " + ("REAL-TIME" if conn_status=="STRONG" else ("DELAYED" if conn_status=="WEAK" else "NO SIGNAL")) + "\n\n"
            "SYNCED SENSOR DATA\n"
            "Radiation  : " + str(round(synced_data["rad"],2)) + " mSv\n"
            "Gas        : " + str(round(synced_data["gas"],2)) + " ppm\n"
            "Temp       : " + str(round(synced_data["temp"],1)) + " C\n"
            "Pressure   : " + str(round(synced_data["pressure"],1)) + " kPa"
        )

        alarm_panel.background = alert_colors[alert_level]
        alarm_panel.text = (
            "ALERT LEVEL " + str(alert_level) + " : " + alert_names[alert_level] + "\n"
            "Gas: " + str(round(gas,2)) + " ppm  |  Rad: " + str(round(radiation,2)) + " mSv  |  Temp: " + str(round(temperature,1)) + " C"
        )

        phase_panel.text       = "  " + phase_labels[scenario_phase] + "   [ T=" + str(round(scenario_timer,1)) + "s ]  "
        phase_panel.background = alert_colors[alert_level]

        zone_panel.text = (
            "ZONE STATUS\n\n"
            "Zone A (Reactor)  : " + str(round(4+random()*2+(1 if scenario_phase>=2 else 0),1)) + " mSv\n"
            "Zone B (Turbine)  : " + str(round(3+random()*1.5,1)) + " mSv\n"
            "Zone C (Pump)     : " + ("DANGER " + str(round(gas,1)) + " ppm" if scenario_phase>=1 else "Normal") + "\n"
            "Zone D (Cooling)  : " + str(round(2+random()*2,1)) + " mSv\n"
            "Control Room      : NO ENTRY (enforced)\n\n"
            "Workers           : " + ("EVACUATED" if scenario_phase>=2 else "On Duty") + "\n"
            "Robot 2           : " + ("ACTIVE" if scenario_phase>=3 else "Standby") + "\n"
            "Containment       : " + ("ACTIVE" if scenario_phase>=5 else "Pending")
        )

        action_log.text = "ROBOT ACTION LOG\n\n" + "\n".join(log_lines)

        # GRAPHS
        temp_curve.plot(time_counter, temperature);  temp_limit.plot(time_counter, 42)
        rad_curve.plot(time_counter,  radiation);    rad_limit.plot(time_counter,  10)
        gas_curve.plot(time_counter,  gas);          gas_limit.plot(time_counter,   3)
        batt_robot.plot(time_counter, robot_battery)
        batt_drone.plot(time_counter, drone_battery)
        batt_low.plot(time_counter,   20)
        alert_curve.plot(time_counter, alert_level)