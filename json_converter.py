# json converter tests, for react stuff

import json

a = [('queen', 0.8407386541366577), ('monarch', 0.7541723847389221), ('prince', 0.7350203394889832), ('princess', 0.696908175945282), ('empress', 0.6771803498268127), ('sultan', 0.6649758815765381), ('Chakri', 0.6451102495193481), ('goddess', 0.6439394950866699), ('ruler', 0.6275452971458435), ('kings', 0.6273427605628967)]


b = json.dumps(a)


print(b)


# out: [["queen", 0.8407386541366577], ["monarch", 0.7541723847389221], ["prince", 0.7350203394889832], ["princess", 0.696908175945282], ["empress", 0.6771803498268127], ["sultan", 0.6649758815765381], ["Chakri", 0.6451102495193481], ["goddess", 0.6439394950866699], ["ruler", 0.6275452971458435], ["kings", 0.6273427605628967]]





