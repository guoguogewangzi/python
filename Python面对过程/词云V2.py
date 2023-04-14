import wordcloud
txt="life if short, you need python"
w = wordcloud.WordCloud(\
        background_color="white"
    )
w.generate(txt)
w.to_file("pywcloud.png")
