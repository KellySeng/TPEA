import hashlib
# from dictionary import Dictionary

def hash_block(block):
    """
    To hash a block we concat the politician, the head, and the letters of the word
    and we hash with sha256
    """
    hasher = hashlib.sha256()
    hasher.update(int(block["politician"], 16).to_bytes(32, byteorder="big"))
    hasher.update(int(block["head"], 16).to_bytes(32, byteorder="big"))
    for letter in block["word"]:
        hasher.update(ord(letter["letter"]).to_bytes(1, byteorder="big"))
    return hasher.hexdigest()

def get_word_from_block(block):
    """
    Return the word corresponding of the block
    """
    word = ""
    for letter in block["word"]:
        word += letter["letter"]
    return word

def is_block_valid(dico,block):
    """
    Return True if the block is valid:
    - the word exist in the dictionary
    - the head of each letter have the same head as the block
    - the letters have different authors
    """
    try:
        if not dico.is_word(get_word_from_block(block)):
            return False
        authors = set()
        for letter in block["word"]:
            if letter["head"] != block["head"]:
                return False
            if letter["author"] in authors:
                return False
            authors.add(letter["author"])
        return True
    except Exception:
        return False

def wordpool_to_trwordpool(dico,wordpool):
    """
    This function transforms the wordpool in a python dictionary easier to manipulate.
    The keys are the hash of a block and the values are the block.
    There is also a field "heads" who stores a set containing all hashes of blocks at the end
    of a chain (only 1 if there are no forks in the blockchain)

    We will call this dictionary trwordpool.
    """
    trwordpool = {
        "heads" : {"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" : None
    }
    for block in wordpool["words"][::-1]: # reverse list:
        add_block(dico,trwordpool,block[1])
    return trwordpool

def add_block(dico,trwordpool,block):
    """
    Add a new block to the trwordpool
    """
    if is_block_valid(dico,block):
        hash_b = hash_block(block)
        trwordpool[hash_b] = block
        trwordpool["heads"].add(hash_b)
        if block["head"] in trwordpool["heads"]:
            trwordpool["heads"].remove(block["head"])

def score_blockchain(dico,trwordpool,hash_b):
    """
    Return the score a the blockchain until hash_b
    """
    block = trwordpool[hash_b]
    score = 0
    while block:
        score += dico.score_word(get_word_from_block(block))
        block = trwordpool[block["head"]]
    return score

def get_best_head(dico,trwordpool):
    """
    Return the hash of the block with the best score in the blockchain
    """
    best_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    best_score = 0
    for hash_b in trwordpool["heads"]:
        tmp_score = score_blockchain(dico,trwordpool,hash_b)
        if tmp_score > best_score:
            best_score = tmp_score
            best_hash = hash_b
    return best_hash

def get_best_blockchain(dico,trwordpool):
    """
    Return the best blockchain from the head to the genesis
    """
    best_head = get_best_head(dico,trwordpool)
    block = trwordpool[best_head]
    res = []
    while block:
        res.append(block)
        block = trwordpool[block["head"]]
    return res

def total_scores(dico,trwordpool):
    """
    Return a the scores of politians and authors from the best blockchain
    """
    best_blockchain = get_best_blockchain(dico,trwordpool)
    scores_authors = {}
    scores_politicians = {}
    for block in best_blockchain:
        # Add score for politician
        if not block["politician"] in scores_politicians:
            scores_politicians[block["politician"]] = 0
        scores_politicians[block["politician"]] += dico.score_word(get_word_from_block(block))

        # Add score for authors
        for letter in block["word"]:
            if not letter["author"] in scores_authors:
                scores_authors[letter["author"]] = 0
            scores_authors[letter["author"]] += dico.score_letter(letter["letter"])
    return scores_politicians,scores_authors

# ====
# Test
# ====

# hash_b1 = hash_block({ "word":[ { "letter":"w", "period":0,
#                      "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#                      "author":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab71",
#                      "signature":"2909ad8ca59787d6421e71e4e9dc807cbbe120892fe9f0d7627d6a6be8746a099fad797884344faff10a892bd1c10bd351f911be05269a3a24f9c5bbace78409" },
#                    { "letter":"z", "period":0,
#                      "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#                      "author":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab73",
#                      "signature":"08efc0569047f34e6cda7410ae2c9aa4d8097438948bc8c3c671cd6b8d309433324ba2e32ecb0fdd2b7aa807a19d6c62957e0d6e9f60897286ff0d9f99bd3106" }
#         ],
#           "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#           "politician":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab78",
#           "signature":"c7a41b5bfcec80d3780bfc5d3ff8c934f7c7f41b27956a8acb20aee066b406edc5d1cb26c42a1e491da85a97650b0d5854680582dcad3b2c99e2e04879769307" })

# wordpool = {
#     "current_period": 0,
#     "next_period": 1,
#     "words": [
#         [0,{ "word":[ { "letter":"a", "period":0,
#                         "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#                         "author":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab71",
#                         "signature":"2909ad8ca59787d6421e71e4e9dc807cbbe120892fe9f0d7627d6a6be8746a099fad797884344faff10a892bd1c10bd351f911be05269a3a24f9c5bbace78409" },
#                       { "letter":"b", "period":0,
#                         "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#                         "author":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab72",
#                         "signature":"08efc0569047f34e6cda7410ae2c9aa4d8097438948bc8c3c671cd6b8d309433324ba2e32ecb0fdd2b7aa807a19d6c62957e0d6e9f60897286ff0d9f99bd3106" }
#         ],
#              "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#              "politician":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab78",
#              "signature":"c7a41b5bfcec80d3780bfc5d3ff8c934f7c7f41b27956a8acb20aee066b406edc5d1cb26c42a1e491da85a97650b0d5854680582dcad3b2c99e2e04879769307" }],

#         [0,{ "word":[ { "letter":"w", "period":0,
#                         "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#                         "author":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab71",
#                         "signature":"2909ad8ca59787d6421e71e4e9dc807cbbe120892fe9f0d7627d6a6be8746a099fad797884344faff10a892bd1c10bd351f911be05269a3a24f9c5bbace78409" },
#                       { "letter":"z", "period":0,
#                         "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#                         "author":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab73",
#                         "signature":"08efc0569047f34e6cda7410ae2c9aa4d8097438948bc8c3c671cd6b8d309433324ba2e32ecb0fdd2b7aa807a19d6c62957e0d6e9f60897286ff0d9f99bd3106" }
#         ],
#              "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#              "politician":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab78",
#              "signature":"c7a41b5bfcec80d3780bfc5d3ff8c934f7c7f41b27956a8acb20aee066b406edc5d1cb26c42a1e491da85a97650b0d5854680582dcad3b2c99e2e04879769307" }]
#     ]
# }

# block = { "word":[ { "letter":"w", "period":0,
#                      "head": hash_b1,
#                      "author":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab71",
#                      "signature":"2909ad8ca59787d6421e71e4e9dc807cbbe120892fe9f0d7627d6a6be8746a099fad797884344faff10a892bd1c10bd351f911be05269a3a24f9c5bbace78409" },
#                    { "letter":"h", "period":0,
#                      "head": hash_b1,
#                      "author":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab72",
#                      "signature":"08efc0569047f34e6cda7410ae2c9aa4d8097438948bc8c3c671cd6b8d309433324ba2e32ecb0fdd2b7aa807a19d6c62957e0d6e9f60897286ff0d9f99bd3106" }
#         ],
#           "head": hash_b1,
#           "politician":"0b418daae4ca18c026d7f1d55237130cbdb9e874d98f7480f85f912c6470ab77",
#           "signature":"c7a41b5bfcec80d3780bfc5d3ff8c934f7c7f41b27956a8acb20aee066b406edc5d1cb26c42a1e491da85a97650b0d5854680582dcad3b2c99e2e04879769307" }

# dico = Dictionary()
# dico.load_file("dict/dict_100000_1_10.txt")
# trwordpool = wordpool_to_trwordpool(dico,wordpool)

# print(trwordpool)
# add_block(dico,trwordpool,block)
# print(trwordpool)
# print(get_best_head(dico,trwordpool))
# print(get_best_blockchain(dico,trwordpool))
# print(total_scores(dico,trwordpool))
