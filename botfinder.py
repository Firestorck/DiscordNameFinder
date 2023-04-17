from unidecode import unidecode
from multiprocessing import Pool, Queue, current_process
import time


TARGET = "Captcha.bot"
MAX_PROCESSES = 16
INPUT_FILE = "names"
OUTPUT_FILE_UNICODE = "unicode_out"
OUTPUT_FILE_VALIDATED = "valid_out"


def split_lst(lst, n):
    print(f"Splitting in {n} parts!")
    return [lst[i::n] for i in range(n)]


def flag_unicode(names):
    flagged_unicode = []
    for name in names:
        if not name.isascii():
            flagged_unicode.append(name)
    unicode_q.put(flagged_unicode)
    print(f"Finished {current_process()}", flush=True)


def verify_target(names):
    verified = []
    for name in names:
        if (unidecode(name) == TARGET):
            verified.append(name)
    verified_q.put(verified)
    if (len(names) > 0):
        print(f"Finished\t{names[0]}\t{names[0].encode('utf-8')}\t{unidecode(names[0]).encode('utf-8')}", flush=True)


def botfinder(names):
    global unicode_q
    global verified_q
#    with open("names") as f:
#        namesfile = f.read()
#    names = namesfile.split("\n")
#    names = list(set(namesfile.split("\n")))
    names = list(set(names))
#    print(f"All names : {names}")
    print(f"Quantity of names found : {len(names)}")

    flagged_unicode = []
    unicode_q = Queue()
    verified = []
    verified_q = Queue()

    print(unicode_q.qsize())
    processes = Pool(MAX_PROCESSES)
    processes.map(flag_unicode, split_lst(names, MAX_PROCESSES))
    print("Waiting for unicode names", end="\r")
    while (unicode_q.qsize() != MAX_PROCESSES and unicode_q != len(names)):
        print(unicode_q.qsize())
        time.sleep(0.5)
    print("Finished finding unicode names. Post-processing", end="\r")
    while not unicode_q.empty():
        flagged_unicode += unicode_q.get()
    print(f"Finished sorting unicode names. Found {len(flagged_unicode)} matches.")
    with open(OUTPUT_FILE_UNICODE, 'w+') as file:
        file.write("\n".join(flagged_unicode))

#    print(f"Flagged with unicode : {flagged_unicode}")

    processes = Pool(MAX_PROCESSES)
    processes.map(verify_target, split_lst(flagged_unicode, MAX_PROCESSES))
    processes.close()
    processes.join()
    while not verified_q.empty():
        verified += verified_q.get()
    print(f"Finished verifiying. Found {len(verified)} matches.")
    with open(OUTPUT_FILE_VALIDATED, 'w+') as file:
        file.write("\n".join(verified))
    return "\n".join(verified)
#    print(f"Flagged 100% target : {verified}")
