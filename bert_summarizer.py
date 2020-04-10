from summarizer import Summarizer
import body as text
import datetime

a = datetime.datetime.now()
model = Summarizer()
b = datetime.datetime.now()
print("Time to load model : ", b-a)

for item in text.body:
    print('Original Text: ', item)
    print("\n")
    c = datetime.datetime.now()
    result = model(item, min_length=60)
    d = datetime.datetime.now()
    print("Inference time", d - c)
    print("\n")
    full = ''.join(result)
    print("Summarized Text: ", full)
    print("\n")
    print("Next Text")

