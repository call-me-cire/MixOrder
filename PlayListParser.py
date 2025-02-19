import itertools
import json
import xml.etree.ElementTree as ET

with open('tonalityToCamelot.json') as json_file:
    tonalityToCamelotValue = json.load(json_file)



class PlaylistParser():
    def __init__(self):
        self.tracks = []
        self.trackIds = []
        self.playListNames = []
        self.file_path = ""
        self.tree = ET.ElementTree

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.tree = ET.parse(file_path)

    def get_playlists(self):
        playlists = self.tree.find("PLAYLISTS").find("NODE[@Name='ROOT']").findall("NODE")
        for playList in playlists:
            self.playListNames.append(playList.get("Name"))

    def parse(self, playlist_name):
        print(playlist_name)
        print("---------------------")
        playlist = self.tree.find("PLAYLISTS").find("NODE[@Name='ROOT']").find(f"NODE[@Name='{playlist_name}']").findall("TRACK")
        track_ids = self.get_track_ids(playlist)

        if len(track_ids) == 0:
            return
        initial_track_list = self.get_initial_track_list(track_ids)
        sorted_track_list = self.sort_in_chunks(initial_track_list)
        self.set_disc_numbers_and_write_to_file(sorted_track_list)
        self.tree.write(self.file_path)



    @staticmethod
    def get_track_ids(playlist):
        track_ids = []

        for track in playlist:
            track_ids.append(track.attrib["Key"])

        return track_ids

    def get_initial_track_list(self, track_ids):
        track_list = []

        for track_id in track_ids:
            track = self.tree.find("COLLECTION").find(f"TRACK[@TrackID='{track_id}']")
            camelot_value = tonalityToCamelotValue[track.attrib.get("Tonality")]
            track_list.append({"name": track.attrib.get("Name"), "camelot": camelot_value, "bpm": float(track.attrib.get("AverageBpm")), "track_id": track_id})

        return track_list

    @staticmethod
    def sort_in_chunks(initial_track_list):
        sorted_by_bpm = sorted(initial_track_list, key = lambda x: (x['bpm']))
        lower = 0.0
        upper = sorted_by_bpm[0]["bpm"] + 5
        chunk = []
        chunks = []

        for index, track in enumerate(sorted_by_bpm):
            if (track['bpm'] <= upper) and (track['bpm'] >= lower):
                chunk.append(track)
            else:
                chunk.append(track)
                chunks.append(chunk)
                chunk = []
                lower = track['bpm']
                upper = track['bpm'] + 5
                if index + 1 == len(initial_track_list):
                    break

        for index, chunk in enumerate(chunks):
            sorted_chunk = sorted(chunk, key=lambda x: (int(x["camelot"][:-1])))
            chunks[index] = sorted_chunk

        return list(itertools.chain(*chunks))

    def set_disc_numbers_and_write_to_file(self, track_list):
        for index, track in enumerate(track_list):
            print(track["name"])
            found_track = self.tree.find("COLLECTION").find(f'TRACK[@TrackID="{track["track_id"]}"]')
            #found_track.set("DiscNumber", str(index + 1))
            found_track.attrib["DiscNumber"] = str(index + 1)
