def get_page(url):
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return ('<html> <body> This is a test page for learning to crawl! '
            '<p> It is a good idea to '
            '<a href="http://www.udacity.com/cs101x/crawling.html">learn to '
            'crawl</a> before you try to  '
            '<a href="http://www.udacity.com/cs101x/walking.html">walk</a> '
            'or  <a href="http://www.udacity.com/cs101x/flying.html">fly</a>. '
            '</p> </body> </html> ')
        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return ('<html> <body> I have not learned to crawl yet, but I '
            'am quite good at '
            '<a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.'
            '</body> </html>')
        elif url == "http://www.udacity.com/cs101x/walking.html":
            return ('<html> <body> I cant get enough '
            '<a href="http://www.udacity.com/cs101x/index.html">crawling</a>! '
            '</body> </html>')
        elif url == "http://www.udacity.com/cs101x/flying.html":
            return ('<html> <body> The magic words are Squeamish Ossifrage! '
            '</body> </html>')
    except:
        return ""
    return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def record_user_click(index,keyword,url):
    urls=lookup(index,keyword)
    if urls:
        for entry in urls:
            if entry[0]==url:
                entry[1]=entry[1]+1    

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append([url, 0])
    else:
        index[keyword] = [[url, 0]]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def split_string(source,splitlist):
    output=[]
    atsplit=True #At a split point
    for char in source: #check each letter
        if char in splitlist:
            atsplit=True
        else:
            if atsplit==True:
                output.append(char)
                atsplit=False
            else:
                output[-1]=output[-1]+char
    return output

def add_page_to_index(index, url, content):
    words = split_string(content, '"!@[]<>,. #¹$;:*/&?=')
    for word in words:
        add_to_index(index, word, url)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index={}
    graph={}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content=get_page(page)
            add_page_to_index(index, page, content)
            outlinks=get_all_links(content)
            graph[page]=outlinks   
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

#Here is an example showing a sequence of interactions:
index = crawl_web('http://www.udacity.com/cs101x/index.html')
#print index
print lookup(index, 'good')
#>>> [['http://www.udacity.com/cs101x/index.html', 0],
#>>> ['http://www.udacity.com/cs101x/crawling.html', 0]]
#record_user_click(index, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#print lookup(index, 'good')
#>>> [['http://www.udacity.com/cs101x/index.html', 0],
#>>> ['http://www.udacity.com/cs101x/crawling.html', 1]]


