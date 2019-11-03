def letterpool_to_trletterpool(letterpool):
    """
    This function transforms the letterpool in a python dictionary easier to manipulate.
    The keys are the hash of a block and the values is a python dictionary with:
    - a field "authors" with all authors that injected a letter for this block
    - a field "letters" containing the list of letters injected for this block

    We will call this dictionary trletterpool.
    """
    trletterpool = {
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" : {"authors" : set(),
                                                                              "letters" : []}
    }
    for letter in letterpool["letters"][::-1]: # reverse list
        add_letter(trletterpool,letter[1])
    return trletterpool

def add_letter(trletterpool,letter):
    """
    Add a letter in trletterpool
    """
    if not letter["head"] in trletterpool:
        trletterpool[letter["head"]] = {
            "authors" : set(),
            "letters" : []
        }
    # An author can't inject a second letter in the same block
    if not letter["author"] in trletterpool[letter["head"]]["authors"]:
        trletterpool[letter["head"]]["authors"].add(letter["author"])
        trletterpool[letter["head"]]["letters"].append(letter)


# ====
# Test
# ====

# trletterpool = {'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855': {'authors': set(), 'letters': []}}
# add_letter(trletterpool,{ "letter":"a", "period":0,
#      "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#      "author":"b7b597e0d64accdb6d8271328c75ad301c29829619f4865d31cc0c550046a08f",
#      "signature":"8b6547447108e11c0092c95e460d70f367bc137d5f89c626642e1e5f2ceb6108043d4a080223b467bb810c52b5975960eea96a2203a877f32bbd6c4dac16ec07"})

# add_letter(trletterpool,{ "letter":"b", "period":0,
#      "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#      "author":"b7b597e0d64accdb6d8271328c75ad301c29829619f4865d31cc0c550046a08f",
#      "signature":"8b6547447108e11c0092c95e460d70f367bc137d5f89c626642e1e5f2ceb6108043d4a080223b467bb810c52b5975960eea96a2203a877f32bbd6c4dac16ec07"})

# add_letter(trletterpool,{ "letter":"c", "period":0,
#      "head":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
#      "author":"b7b597e0d64accdb6d8271328c75ad301c29829619f4865d31cc0c550046a081",
#      "signature":"8b6547447108e11c0092c95e460d70f367bc137d5f89c626642e1e5f2ceb6108043d4a080223b467bb810c52b5975960eea96a2203a877f32bbd6c4dac16ec07"})
