import hashlib

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
        if not (hash_b in trwordpool):
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
        elif tmp_score == best_score:
            if int(hash_b,16) > int(best_hash,16):
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
