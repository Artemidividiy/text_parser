from datetime import datetime
import math
from docx import Document
from rich.console import Console
import json

INPUT_FILE_PATH = "./test.docx"
OUTPUT_FILE_PATH = "./output/result.json"
CHUNK_LENGTH = 2048

class Parser: 
    def __init__(self) -> None:
        self.console = Console()
        self.chunk_count = -1
        self.initialize()

    def find_last_space(self,chunk: str): 
        last_position = -1
        for i in range(1, len(chunk)):
            if chunk[i] == " ": last_position = i
        return last_position

    def get_remaining_word(self,chunk: str): 
        last_space = self.find_last_space(chunk=chunk)
        return chunk[last_space::]

    def chunker(self,text: str, chunk_length: int) -> list[str]:
        self.chunk_count = int(len(text) / chunk_length) + 1
        start_time = datetime.now()
        target = ["" for i in range(self.chunk_count)]
        cur_chunk = 0
        for i in range(0, len(text) - chunk_length, chunk_length):
            if text[i+chunk_length] not in ("\n", " " , "."):
                tmp_target = text[i: i + self.find_last_space(text[i: i+chunk_length])]
                remaining_word = self.get_remaining_word(text[i:i+chunk_length])
                target[cur_chunk] += tmp_target
                target[cur_chunk + 1] += remaining_word
            else: 
                target[cur_chunk] = text[i: i + chunk_length]
            cur_chunk += 1
        if len(text) % chunk_length != 0: 
            target[-1] = "".join(reversed(text[len(text): cur_chunk: -1]))

        # chunks = [text[i:i+chunk_length] for i in range(0, len(text), chunk_length)]    
        self.console.print(f"[green] text was successfully divided by chunks [/green] | time: +{datetime.now() - start_time}")
        return target

    def change_encoding(self,text: str): 
        target = text.encode("ascii", "ignore")
        return target.decode()

    def write_result(self,chunks: list[str], file_path: str): 
        with open(OUTPUT_FILE_PATH, 'w') as file:
            json.dump(self.prettify_chunks(chunks), fp=file)
        self.console.print(f"[green] result writen into {file_path} [/green]")

    def parse_file(self,file_path: str):
        doc = Document(file_path)
        target = ""
        for para in doc.paragraphs:
            text = para.text
            
            target += text + "\n"
        return target

    def prettify_chunks(self,chunks: list[str]): 
        return [
            {
                "chunk number": i,
                "chuck length": len(chunks[i]), 
                "chunk": chunks[i]
            } for i in range(len(chunks))]

    def initialize(self,): 
        self.console.print(f"[cyan] initializing at {datetime.now()} [/cyan]")
        self.console.print(f"[cyan] trying to parse chunks from given text at path: {INPUT_FILE_PATH}")
        ascii_text = self.change_encoding(self.parse_file(INPUT_FILE_PATH))
        
        self.chunks = self.chunker(ascii_text, CHUNK_LENGTH)
        self.console.log(f"chunks count: {self.chunk_count}")
        self.write_result(self.chunks, OUTPUT_FILE_PATH)
    def return_map(self): 
        return self.prettify_chunks(self.chunks)
    
    def return_json(self): 
        return json.dumps(self.return_map())


if __name__ == "__main__": 
    parser = Parser()
    parser.initialize()