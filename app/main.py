from converter import OvalToJsonConverter
from config import filepath

if __name__ == '__main__':
    converter = OvalToJsonConverter()
    converter.convert(filepath)
