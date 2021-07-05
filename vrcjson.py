import tkinter as tk
import tkinter.messagebox

from tkinter import filedialog

import os, json
import traceback # End user

rootwin = tk.Tk()
rootwin.title("VRCJSON - VRChat config file GUI * by DJ3520")

file = os.getenv('USERPROFILE') + "\\AppData\\LocalLow\\VRChat\\VRChat\\config.json"

def insure_int(val):
  return val.isdigit() or val == ""

cache_directory = tk.StringVar()

def reset_folder():
  cache_directory.set("")

def choose_folder():
  folder = filedialog.askdirectory(title="Choose new location for VRChat cache.", initialdir=os.getenv('USERPROFILE') + "\\AppData\\LocalLow\\VRChat\\VRChat", mustexist=True)
  if not os.path.isdir(folder): folder = ""
  cache_directory.set(folder)

verify=(rootwin.register(insure_int))

save_settings_button = tk.Button(rootwin, text="Click this button to save updated settings to file.")
save_settings_button.pack(side=tk.TOP, fill=tk.X)

# Cache settings
cache = tk.LabelFrame(rootwin, text="Cache settings")
cache.pack(side=tk.TOP, fill=tk.X)

tk.Button(cache, text="Choose cache location", command=choose_folder).grid(row=0, column=0)
reset_location = tk.Button(cache, text="Reset cache location", command=reset_folder)
reset_location.grid(row=0, column=1)
cache_size = tk.StringVar()
tk.Label(cache, text="Maximum cache size in GB: ").grid(row=1, column=0)
tk.Entry(cache, textvariable=cache_size, width=6, validate='all', validatecommand=(verify, '%P')).grid(row=1, column=1)
cache_expiry_time = tk.StringVar()
tk.Label(cache, text="Days before item in cache is deleted: ").grid(row=2, column=0)
tk.Entry(cache, textvariable=cache_expiry_time, width=6, validate='all', validatecommand=(verify, '%P')).grid(row=2, column=1)

def update_reset(*args):
  if cache_directory.get() == "": reset_location.config(state=tk.DISABLED)
  else: reset_location.config(state=tk.NORMAL)

cache_directory.trace('w', update_reset)
cache_directory.set("")

# Rich presence
richpres = tk.LabelFrame(rootwin, text="Discord and Steam integration")
richpres.pack(side=tk.TOP, fill=tk.X)
disableRichPresence = tk.BooleanVar()
tk.Checkbutton(richpres, text="Show your location in Discord and Steam.", variable=disableRichPresence).grid(row=0)
disableRichPresence.set(True)

# Dynbone limiter
dynbones = tk.LabelFrame(rootwin, text="Dynamic Bone Limiter")
dynbones.pack(side=tk.TOP, fill=tk.X)
tk.Label(dynbones, text="Maximum amount of objects/bones movable by dynamic bones per avatar: ").grid(row=0, column=0)
dynamic_bone_max_affected_transform_count = tk.StringVar()
tk.Entry(dynbones, textvariable=dynamic_bone_max_affected_transform_count, width=4, validate='all', validatecommand=(verify, '%P')).grid(row=0, column=1)
tk.Label(dynbones, text="Maximum amount of dynamic bone colliders per avatar: ").grid(row=1, column=0)
dynamic_bone_max_collider_check_count = tk.StringVar()
tk.Entry(dynbones, textvariable=dynamic_bone_max_collider_check_count, width=4, validate='all', validatecommand=(verify, '%P')).grid(row=1, column=1)

# Picture settings
pictures = tk.LabelFrame(rootwin, text="Camera and screenshot settings")
pictures.pack(side=tk.TOP, fill=tk.X)
camera_res_height = tk.StringVar()
camera_res_width = tk.StringVar()
screenshot_res_height = tk.StringVar()
screenshot_res_width = tk.StringVar()
camera_res_height.set("1080")
camera_res_width.set("1920")
screenshot_res_height.set("1080")
screenshot_res_width.set("1920")
tk.Label(pictures, text="VR Camera picture size: ").grid(row=0, column=0)
tk.Spinbox(pictures, textvariable=camera_res_width, width=4, from_=1280, to=3840).grid(row=0, column=1)
tk.Spinbox(pictures, textvariable=camera_res_height, width=4, from_=720, to=2160).grid(row=0, column=2)
tk.Label(pictures, text="Desktop screenshot picture size: ").grid(row=1, column=0)
tk.Spinbox(pictures, textvariable=screenshot_res_width, width=4, from_=1280, to=3840).grid(row=1, column=1)
tk.Spinbox(pictures, textvariable=screenshot_res_height, width=4, from_=720, to=2160).grid(row=1, column=2)

# Particle limiter
particles = tk.LabelFrame(rootwin, text="Particle limiter settings")
particles.pack(side=tk.TOP, fill=tk.X)
particle_system_limiter = tk.BooleanVar()
tk.Checkbutton(particles, text="Enable particle system limiter.", variable=particle_system_limiter).grid(row=0)
ps_max_particles = tk.StringVar()
ps_max_systems = tk.StringVar()
ps_max_emission = tk.StringVar()
ps_max_total_emission = tk.StringVar()
ps_mesh_particle_divider = tk.StringVar()
ps_mesh_particle_poly_limit = tk.StringVar()
ps_collision_penalty_high = tk.StringVar()
ps_collision_penalty_med = tk.StringVar()
ps_collision_penalty_low = tk.StringVar()
ps_trails_penalty = tk.StringVar()
tk.Label(particles, text="Max particles per system: ").grid(row=1, column=0)
tk.Entry(particles, textvariable=ps_max_particles, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=1, column=1)
tk.Label(particles, text="Max particles systems per avatar: ").grid(row=2, column=0)
tk.Entry(particles, textvariable=ps_max_systems, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=2, column=1)
tk.Label(particles, text="Max speed of particle creation per system: ").grid(row=3, column=0)
tk.Entry(particles, textvariable=ps_max_emission, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=3, column=1)
tk.Label(particles, text="Max speed of particle creation per avatar: ").grid(row=4, column=0)
tk.Entry(particles, textvariable=ps_max_total_emission, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=4, column=1)
tk.Label(particles, text="Divide highest mesh particle polygon count: ").grid(row=5, column=0)
tk.Entry(particles, textvariable=ps_mesh_particle_divider, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=5, column=1)
tk.Label(particles, text="Highest polygon count per mesh particle: ").grid(row=6, column=0)
tk.Entry(particles, textvariable=ps_mesh_particle_poly_limit, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=6, column=1)
tk.Label(particles, text="Penalty for high accuracy collision: ").grid(row=7, column=0)
tk.Entry(particles, textvariable=ps_collision_penalty_high, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=7, column=1)
tk.Label(particles, text="Penalty for medium accuracy collision: ").grid(row=8, column=0)
tk.Entry(particles, textvariable=ps_collision_penalty_med, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=8, column=1)
tk.Label(particles, text="Penalty for low accuracy collision: ").grid(row=9, column=0)
tk.Entry(particles, textvariable=ps_collision_penalty_med, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=9, column=1)
tk.Label(particles, text="Penalty for trails on particles: ").grid(row=10, column=0)
tk.Entry(particles, textvariable=ps_trails_penalty, width=10, validate='all', validatecommand=(verify, '%P')).grid(row=10, column=1)

matchup = {
  "particle_system_limiter"                  : particle_system_limiter,
  "ps_max_particles"                         : ps_max_particles,
  "ps_max_systems"                           : ps_max_systems,
  "ps_max_emission"                          : ps_max_emission,
  "ps_max_total_emission"                    : ps_max_total_emission,
  "ps_mesh_particle_divider"                 : ps_mesh_particle_divider,
  "ps_mesh_particle_poly_limit"              : ps_mesh_particle_poly_limit,
  "ps_collision_penalty_high"                : ps_collision_penalty_high,
  "ps_collision_penalty_med"                 : ps_collision_penalty_med,
  "ps_collision_penalty_low"                 : ps_collision_penalty_low,
  "ps_trails_penalty"                        : ps_trails_penalty,
  "dynamic_bone_max_affected_transform_count": dynamic_bone_max_affected_transform_count,
  "dynamic_bone_max_collider_check_count"    : dynamic_bone_max_collider_check_count,
  "cache_directory"                          : cache_directory,
  "disableRichPresence"                      : disableRichPresence,
  "camera_res_height"                        : camera_res_height,
  "camera_res_width"                         : camera_res_width,
  "screenshot_res_height"                    : screenshot_res_height,
  "screenshot_res_width"                     : screenshot_res_width,
  "cache_expiry_time"                        : cache_expiry_time,
  "cache_size"                               : cache_size
}

if os.path.isfile(file):
  with open(file) as f:
    settings = json.load(f)
  # Slightly different between how we internally handle this and how VRC expects the save to be organized.
  if not "betas" in settings.keys():
    settings["betas"] = []
  settings["particle_system_limiter"] = "particle_system_limiter" in settings["betas"]
  del settings["betas"]
  for k, v in matchup.items():
    if k in settings.keys():
      if k == "disableRichPresence": v.set(not settings[k])
      else: v.set(settings[k])

def save_settings():
  try:
    global matchup
    settings = {}
    for k, v in matchup.items():
      if k == "disableRichPresence": settings[k] = not v.get()
      else: settings[k] = v.get()
      print(k, v.get())
      if isinstance(settings[k], str):
        if settings[k].isdigit():
          settings[k] = int(settings[k])
        elif settings[k] == "":
          del settings[k]

    # Slightly different between how we internally handle this and how VRC expects the save to be organized.
    if settings["particle_system_limiter"]:
      settings["betas"] = ["particle_system_limiter"]
    del settings["particle_system_limiter"]

    savestr = json.dumps(settings, indent=2)
    with open(file, 'w') as f:
      f.write(savestr)
    tkinter.messagebox.showinfo(title="Save successful.", message="New settings saved to config.json file. VRChat will need to be restarted for these changes to take effect.")
  except Exception as e:
    with open('error.txt', 'a') as f:
      f.write(str(e))
      f.write(traceback.format_exc())
    tkinter.messagebox.showwarning(title="Save failed!", message="Something happened during the file save. Please report this to the GitHub and upload the error.txt file.")

save_settings_button.config(command=save_settings)

if not os.path.isdir(os.getenv('USERPROFILE') + "\\AppData\\LocalLow\\VRChat\\VRChat"):
  tkinter.messagebox.showerror(title="Folder not found", message="Could not find folder where VRChat expects the settings file to exist.")
  raise SystemExit

rootwin.resizable(tk.FALSE, tk.FALSE)
rootwin.mainloop()