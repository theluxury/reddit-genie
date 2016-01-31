from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast

# Read the whole text.
text = open('meh.txt').read()
print text
text = ast.literal_eval(text)


# Generate a word cloud image
wordcloud = WordCloud().generate_from_frequencies(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
