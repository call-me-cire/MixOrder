mixOrder.py import json
import xml.etree.ElementTree as ET

with open('tonalityToCamelot.json') as json_file:
    tonalityToCamelotValue = json.load(json_file)

file = "/Users/muckbuck/Documents/Tracks/Rekordbox/Rekordbox.xml"
tree = ET.parse(file)
tracks = []
playList = tree.find("PLAYLISTS").find("NODE[@Name='ROOT']").find("NODE[@Name='MIK Cue Points']").findall("TRACK")
trackIds = []

for track in playList:
    trackIds.append(track.attrib["Key"])

for trackId in trackIds:
    track = tree.find("COLLECTION").find(f"TRACK[@TrackID='{trackId}']")
    camelotValue = tonalityToCamelotValue[track.attrib.get("Tonality")]
    tracks.append({"name": track.attrib.get("Name"), "camelot": camelotValue, "bpm": float(track.attrib.get("AverageBpm"))})

sortedByBpm = sorted(tracks, key = lambda x: (x['bpm'], x['camelot']))
#print(json.dumps(sortedByBpm,sort_keys=False, indent=4))
for index, track in enumerate(sortedByBpm):
    print(f"BPM: {track['bpm']} KEY: {track['camelot']} NAME: {track['name']}")
    trackName = sortedByBpm[index]["name"]
    fisk = tree.find("COLLECTION").find(f'TRACK[@Name="{trackName}"]')
    fisk.set("DiscNumber", str(index + 1))
    tree.write(file)
