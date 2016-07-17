# How similar are my operating systems?
A question that has spun out of one of my projects that I suspect would be useful in many applications but hasn't been fully explored is comparison of operating systems. If you think about it, for the last few decades we've generated many methods for comparing differences between files. We have [md5]() sums to make sure our downloads didn't poop out, and [command line tools]() to quickly look for differences. We now have to take this up a level, because our new level of operation isn't on a single "file", it's on an entire operating system. It's not just your Mom's computer, it's a container-based thing (e.g., [Docker]() or [Singularity]()) that contains a base OS plus additional libraries and packages and then the special sause, the application or analysis that the container was birthed into existence to carry out. It's not good enough to have message storage places to dump these containers, we need simple and consistent methods to computationally compare them, organize them, and let us explore them.


# Similarity of File Paths
When I think about it, an entire understanding of an "image" (or more generally, a computer or operating system) comes down to the programs installed, and files included. Yes, there might be various environmental variables, but I would hypothesize that the environmental variables found in an image have a rather strong correlation with the software installed, and we would do pretty well to understand the guts of an image from the body without the electricity flowing through it. This would need to be tested, but not quite yet.

Thus, since we are working in linux land, our problem is simplified to comparing file and folder paths. We have lists of both of those things exported by [singularity-python](http://www.github.com/singularityware/singularity-python) with [these scripts](../docker). We can simplify this idea even further - each file path is like a list of sorted words. Comparing two images comes down to comparing these lists, and in this operation there are two comparisons we are interested in:

 - comparing a single file path to a second path, within the same image, or from another image
 - comparing an entire set of file paths (one image) to a (?somewhat) different set (a second image).


### Comparison of two images
I would argue that this is the first level of comparison, meaning the rougher, higher level comparison that asks "how similar are these two things, broadly?" In this framework, I want to think about the image paths like features, and so a similarity calculation can come down to comparing two sets of things, and I've made [a function](https://github.com/singularityware/singularity-python/blob/master/singularity/package.py#L90) to do this. It comes down to a ratio between the things they have in common (intersect) over the entire set of things:

      score = 2.0*len(`intersect`) / (len(`pkg1`)+len(`pkg2`))

I wasn't sure if "the entire set of things" should include just folder paths, just files paths, or both, and so I decided to try all three approaches. It also would need to be determined if we can further streamline this approach by filtering down the paths first. For example, take a look at the paths below:

      ./usr/include/moar/6model',
      ./usr/include/moar/6model/reprs'

We don't **really** need the first one because it's represented in the second one. However, if some Image 1 has the first but not the second (and we are doing a direct comparison of things) we would miss this overlap. Thus, let's say we have some pipeline that aims to map an image into it's correct spot on some graph. I would do something like the following:


## Generating a rough graph of images

1. Start with a big list of (likely) base containers (e.g., Docker library images)
2. Derive a similarity scores based on the rough approach above. We can determine likely parents / children based on one image containing all the paths of another plus more (a child), or a subset of the paths of the other (a parent). This will give us a bunch of tiny graphs, and pairwise similarity scores for all images.
3. Within the tiny graphs, define potential parent nodes (images) as those that have not been found to be children of any other images.
4. For all neighbors / children within a tiny graph, do the equivalent comparison, but now on the level of files to get a finer detail score.
5. Find a strategy to connect the tiny graphs. The similarity scores can do well to generate a graph of all nodes, but we would want a directional graph with nice detail about software installed, etc.

Points 3-5, but I'm not ready yet to think about how to fine tune the graph given that I need to build it first. Actually, if I use Docker files that have a clear statement about the "parent" image, I could see how well the approach does to find those relationships based on the paths alone.


## Classifying a new image into this space
Generating a rough graph isn't too wild an idea, as we've seen above. The more challenging, and the reason that this functionality is useful, is quickly classifying a new image into this space. Why? I'd want to, on the command line, get either a list or open a web interface to immediately see the differences between two images. I'd want to know if the image that I made is similar to something already out there, or if there is a base image that removes some of the redundancy for the image that I made. In this visualization I'd want

Now we have some special cases, specifically, these are base images. Base images are those "official" Docker library images like Ubuntu, or Nginx, or postgres that many others are likely to build off of. There are also several ways to identify what should be a "base" image: it is likely the case that people will add on to base images, and it is less likely they will subtract from them. Thus, a base image can be found by doing the following:

- Parse a crapton of Docker files, and find the images that are most frequently used
- Logically, an image that extends some other image is a child of that image. We can build a graph/tree based on this
- We can cut the tree at some low branch to define a core set of bases.

To classify a new image into this tree space, we don't need to do pairwise comparisons of that new image with every image - we need to do graph comparisons, or start with the base sets, and then walk down the tree following the path of highest similarity. If we hit a node where the new image has fewer things than the previous base, we probably went too far. We can minimally figure out (with some confidence) where the image fits in this tree based on this algorithm, and very likely find redundancy in installation (for example, many people may extend a base image and do custom installs that are already presented in a lower branch base and thus uncessary).


### Comparison of single paths
Within an image, we have some redundancy in paths that are simply longer versions of others. For example:

      ./usr/include/moar/6model',
      ./usr/include/moar/6model/reprs'

I know that the first must exist by way of the second! Thus, I might argue that it would be kind of stupid to include both of these paths in a comparison with another image. However, filtering down to a base set (for an image) is still going to require a good bit of comparison. But wait, let's remember that this is sorted, and it's sorted from simplier --> more complex paths. Here are some questions that I want to answer, to help me figure this out:

   - How many folders / files are included in each "base" image?
   - Of those included, how many are simply extensions off of a parent?

Now that I think about it, I think I have two interesting ideas for representations. If I represent an image as a graph/tree, then I can figure out if a second image is an extension of it based on it being a subgraph. I can also model the paths as being documents in a corpus, and compare corpus based on having similar documents. Maybe I'll try visualizing the graph/tree first, this might be useful to see anyway!

**STILL THINKING**


