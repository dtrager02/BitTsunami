import os
import json
import hashlib
import time
import sys
import base64
from unicodedata import name
class Request:
    def __init__(self,file_id,offset,value,length=16) -> None:
        self.file_id = file_id
        self.offset = offset
        self.value = value
        self.hash = self.get_chunk_hash()
    def __repr__(self) -> str:
        return ";".join([self.file_id,self.offset,self.value])
    def get_chunk_hash():
        ...

class Connection:
    def __init__(self) -> None:
        """_summary_
        recursively walk local directory and get hashes of files
        #open a socket to be ready for file requests
        #allow user to select which files to seed
        send list of hashes of seeded files to tracker
        """
        ...
    def __repr__(self) -> str:
        """_summary_
        this is the connection string that will be sent to tracker for any changes
        ip|port|
        ip|port|
        """
    def request_chunk(self):
        ...
        # make request object, pickle it, send it to tracker
    def modify_seeds(self):
        ...
    def download_file(self):
        ...
    def user_input_loop(self):
        ...
    def parse_torrent_file(self):
        ...
    def validate_checksum(self,request:Request,data):
        ...
    def update_tracker(self):
        """_summary_
        Run periodically to tell tracker which files are available
        add or remove connection from tracker when starting/closing
        """
        

class Tracker:
    def __init__(self) -> None:
        """_summary_
        open server for connections
        store data like torrent1 -> connection1, -> avaliable chunks
                                    connection2 -> avaliable chunks
        """
    def add_connection(self,connection_string):
        """_summary_
        Adds a client to the tracker with their ip, port, and available torrents
        """
        ...
    def remove_connection(self,connection_string):
        """_summary_
        Removes a client to the tracker with their ip, port, and available torrents
        """
        ...
    def assign_peer(self,request:Request, torrent_id,chunk_id):
        """_summary_
        find a peer to give the leecher the requested chunk
        """
class TorrentGenerator:
    def __init__(self,path,piece_size = 1024**2) -> None:
        self.path = path
        self.piece_size = piece_size
    def generate_torrent_file(self):
        tracker = "put get request url for announce here"
        info = dict()
        info["name"] = os.path.basename(os.path.normpath(self.path))
        info["announce"] = tracker
        info["piece_size"] = self.piece_size
        info["piece_encoding"] = "Base64"
        info["files"],info["pieces"] = [],[]
        #this will be replaced by the tail of the nth file
        self.buffer = bytearray()
        files_in_current_piece = {} #tracking smaller files for debugging purposes
        for dirpath, dirnames, filenames in os.walk(self.path):
            for name in filenames:
                filepath = os.path.join(dirpath, name)
                with open(filepath,"rb") as f:
                    # add file to ordered list of files
                    size = os.path.getsize(filepath)
                    info["files"].append({"path":os.path.relpath(filepath,start=self.path),"size":size}) 
                    #read as much as possible up to buffer size
                    a = f.read(self.piece_size-len(self.buffer))
                    while len(a):
                        self.buffer.extend(a)
                        #this case means the file read was not large enough to create a new piece or we reached the end of a file
                        if len(self.buffer) < self.piece_size:
                            # caching files within current piece for debugging
                            files_in_current_piece[filepath] = len(a)
                            print(f"File did not fill piece size buffer... Current piece includes bytes from: {str(files_in_current_piece)} ")
                            break
                        #this case means the file piece filled the piece buffer
                        files_in_current_piece.clear()
                        print(f"Calculating Hash for {filepath}...")
                        piece = TorrentGenerator.get_hash_piece(self.buffer) #returns sha1 hash
                        self.buffer = bytearray() #reset buffer
                        info['pieces'].append(piece) #number of pieces per file should be \ceil file_size/self.piece_size
                        #read next subpiece
                        a = f.read(self.piece_size)
                        
        #This SHOULD add the last remaining piece to the list                
        #piece = TorrentGenerator.get_hash_piece(self.buffer) #returns sha1 hash
        #self.buffer = bytearray() #reset buffer
        #info['pieces'].extend(piece) #number of pieces per file should be \ceil file_size/self.piece_size
        with open(f"{info['name']}_meta.json","w+") as output:
            json.dump(info,output)
        return info

    @staticmethod
    def get_hash_piece(bytes : bytearray): # 2 MB piece size default
        m = hashlib.sha1() #sha1 has a 20 bytedigest size and 512 byte block size
        m.update(bytes)
        return base64.b64encode(m.digest()).decode()
    
    def hash_accuracy_test(self):
        #testing production code
        info1 = self.generate_torrent_file()
        #janky simple test that should produce same output
        filecontent = bytearray()
        for dirpath, dirnames, filenames in os.walk(self.path):
            for name in filenames:
                filepath = os.path.join(dirpath, name)
                with open(filepath,"rb") as f:
                    filecontent.extend(f.read())
        i = 0
        pieces = []
        while i < len(filecontent):
            pieces.append(TorrentGenerator.get_hash_piece(filecontent[i:i+self.piece_size]))
            i+= self.piece_size
        if pieces == info1["pieces"]:
            print("Test successful")
        else:
            temp = list(zip(pieces,info1["pieces"]))
            for i in range(len(temp)):
                if temp[i][0] != temp[i][1]:
                    print(f"{temp[i][0]} , {temp[i][1]}, {i}")

        

if __name__ == "__main__":
    start = time.time()
    #print(get_hash_pieces("./ds_4X_96fps.mp4")[:20])
    torrent = TorrentGenerator("./youtube")
    torrent.hash_accuracy_test()
    print(time.time()-start)