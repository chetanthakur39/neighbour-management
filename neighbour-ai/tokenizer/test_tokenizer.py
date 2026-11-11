from tokenizer import SimpleTokenizer


texts = [
    "Show invalid neighbours in Uttar Pradesh",
    "Delete invalid neighbours in Uttar Pradesh for JC_Lucknow",
    "Check PCI and TAC validity",
    "Show cleanup progress"
]


tokenizer = SimpleTokenizer(vocab_size=2000)

tokenizer.train(texts)


print("Vocabulary size:", len(tokenizer))


text = "Delete invalid neighbours in Uttar Pradesh"

encoded = tokenizer.encode(text)

print("\nOriginal:")
print(text)

print("\nEncoded:")
print(encoded)

print("\nDecoded:")
print(tokenizer.decode(encoded))