import pytholog as pl
import aiml

k = aiml.Kernel()
k.learn("udc.aiml")

fact = pl.KnowledgeBase("parent")
fact2 = pl.KnowledgeBase("parent")
fact3 = pl.KnowledgeBase("parent")

fact(["isFatherof(X,Y)"])
fact2(["isMotherof(X,Y)"])
fact3(["isFriendof(X,Y)"])

while True:
    inputText = input("User>>")
    if inputText == "bye":
        print("Bye")
        break
    else:
        resp = k.respond(inputText)
        Father = k.getPredicate("father")
        Mother = k.getPredicate("mother")
        Friend = k.getPredicate("friend")

        if Father:
            print(Father)
            print(fact.query(pl.Expr("isFatherof(Father,athar)")))
            print("bot>>", resp)
        if Friend:
            print(Friend)
            print(fact3.query(pl.Expr("isFriendof(Friend,athar)")))
            print("bot>>", resp)

        if Mother:
            print(Mother)  # Corrected from "Father"
            print(fact2.query(pl.Expr("isMotherof(Mother,athar)")))
            print("bot>>", resp)

        else:
            print("NOTHING TO SHOW")
