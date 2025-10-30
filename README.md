# FOSS4GNA 2025 Graph Visualizer

[View Interactive Graph](https://www.rachelgugler.com/projects/2025-10-29_foss4g_graph_map/)

There are over 120 and workshops and talks at the 2025 FOSS4GNA Conference in Reston, VA (November 3-5), and the system limits submitting talk and workshops into a single track when they often fit multiple tracks. I wanted a better understanding of the options, so I decided to do some extra visualization. This was also my first time using Claude AI. It definitely sped up the data preparation. For a higher stakes project I would definitely do more QC on the data from the amount of wrangling I had to do with the Python code, but being that this is a low risk situation to not do that, I didn't do very much data QC.

## Data Preparation
1. Workshops don't have Tracks, so I assigned those to the best of my understanding of the topic.
2. I used Claude AI to analyze the talk/workshop descriptions and abstracts and had it assign up to 3 additional tracks it could also fit into.
3. I did some very brief data QC, but I make no promises there are not errors.

## The Script

I originally prompted Claude to make 2 versions of an mvp project to make an interactive graph map. The first version was to use Pyvis and be embedable in a Quarto website for my portfolio, the 2nd it could use any technology it thought would be good, but it also had to be embedable into a website. I read an article recently that asking AI for multiple options helps offer more creative answers, so that is what the goal was for this. My original goal was to use Pyvis, so that is the option I went with. For the 2nd option, it chose to make a regualr html file with embedded css and javascript and it did not work. I'm sure some debugging would have made it work, but I continued with Pyvis.

I did have to do quite a lot of back and forth with it debugging the original outputs before getting a usable v1 would consider putting online. I forgot to tell it I was using UV initially, so I had to have it reformat everything into using functions early on. 

## Conclusion

I watched most of the Youtube series [How to Use PyVis Library in Python Tutorials](https://youtube.com/playlist?list=PL2VXyKi-KpYu7djT-8bDxtylvxznz3WLR&si=EFKfpOAsftlLfuoI) when working on this project. Overall I am very happy with the output versus how much time I took to make it. 

I have a better understanding of graphs now, however I don't think I would have that understanding if it wasn't for watching the videos. If I was going to make a graph with different data, I would do a lot more coding based on reading documentation to have a better understanding of each part of the code. It would have taken me longer to debug and give useful prompts without my prior coding experience.