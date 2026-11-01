import time
from threading import Thread, Lock


sentences: list[str] = []  # 1000 Sentences

with open("dummy_sentences.txt", "r") as sentences_file:
  sentences = sentences_file.readlines()

print(sentences)

sentences_set_1: list[str] = sentences[:500]
sentences_set_2: list[str] = sentences[500:]

print(sentences_set_1)
print("===========================================================================================")
print(sentences_set_2)

def get_vowel_info_for_sentence(curr_sentence: str) -> dict[str, int]:
  vowel_info: dict[str, int] = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
  for curr_char in curr_sentence:
    if curr_char in ["a", "e", "i", "o", "u"]:
      vowel_info[curr_char] = vowel_info[curr_char] + 1
  return vowel_info

def process_sentence_set(curr_sentence_set):
  # Start Processing Set 1
  for curr_sentence in curr_sentence_set:
    curr_sentence_vowels_info: dict[str, int] = get_vowel_info_for_sentence(curr_sentence)
    print(curr_sentence_vowels_info)


t1 = Thread(target=process_sentence_set, args=(sentences_set_1,))
t2 = Thread(target=process_sentence_set, args=(sentences_set_2,))

start_time = time.time()  # Epoch time (seconds passed since Jan 1970)
t1.start()
t2.start()

t1.join()
t2.join()
processing_time = time.time() - start_time
print(f"Time it took in seconds: {processing_time}")  # 0.14040207862854004 for async

# start_time = time.time()  # Epoch time (seconds passed since Jan 1970)
# process_sentence_set(sentences_set_1)
# print("===========================================================================================")
# process_sentence_set(sentences_set_2)
# processing_time = time.time() - start_time
# print(f"Time it took in seconds: {processing_time}")  # 0.055638790130615234 for Sync