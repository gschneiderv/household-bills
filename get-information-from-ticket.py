import os
from time import perf_counter
from typing import NamedTuple
from concurrent.futures import ProcessPoolExecutor
import json

from paddleocr import PaddleOCR, draw_ocr
from more_itertools import collapse

ocr = PaddleOCR(lang="en") 

# Initialize a dictionary to store the shoppings for each supermarket
data_per_receipe = {}
error_receipe = set()

tickets_path = "/Users/andreslaurito/repos/household-bills/household-bills/tickets"

class OCRResult(NamedTuple):
    text: str
    name: str

def process_image(img_path:str) -> str:
    print(f"Detecting {img_path}")
    result = ocr.ocr(f'{tickets_path}/{img_path}')
    text = [text for text in collapse(result) if type(text) == str]
    return OCRResult(text=text, name=img_path)

def main() -> None:
    t0 = perf_counter()
    try:
        with ProcessPoolExecutor() as executor:
            for res in executor.map(process_image, os.listdir(tickets_path)):
                print("Got result for ", res.name)
                data_per_receipe[res.name] = res.text
    except Exception as e:
        print(f"Error processing image: {e}")
        error_receipe.add(e)
            
    elapsed_time = perf_counter() - t0
    print(f"Took {elapsed_time}s to apply ocr in all tickets")

    output = json.dumps(data_per_receipe, indent=4)
    print("Writing json output")
    with open('reciepes.json', 'w') as fp:
        fp.write(output)

    
if __name__ == '__main__':
    main()
