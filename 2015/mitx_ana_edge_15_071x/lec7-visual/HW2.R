library(ggplot2)
library(ggmap)

install.packages("igraph")
library(igraph)

edges = read.csv("edges.csv")
users = read.csv("users.csv")
str(edges)
str(users)

292/59

g = graph.data.frame(edges, FALSE, users)
plot(g, vertex.size=5, vertex.label=NA)
degree(g)
table(degree(g) >= 10)
V(g)$size = degree(g)/2+2
plot(g, vertex.label=NA)

V(g)$color = "black"
V(g)$color[V(g)$gender == "A"] = "red"
V(g)$color[V(g)$gender == "B"] = "gray"
plot(g, vertex.label=NA)


V(g)$color = "black"
V(g)$color[V(g)$school == "A"] = "red"
V(g)$color[V(g)$school == "AB"] = "gray"
plot(g, vertex.label=NA)

V(g)$color = "black"
V(g)$color[V(g)$locale == "A"] = "red"
V(g)$color[V(g)$locale == "B"] = "gray"
plot(g, vertex.label=NA)

plot.igraph(g, vertex.label=NA)

