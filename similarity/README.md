# Similarity of File Paths

How do we calculate similarity of two images? When you think about it, an entire understanding of an "image" (or more generally, a computer or operating system) comes down to the programs installed, and files included. Yes, there might be various environmental variables, but I would hypothesize that the environmental variables found in an image have a rather strong correlation with the software installed, and we would do pretty well to understand the guts of an image from the body without the electricity flowing through it. This would need to be tested, but not quite yet.

Thus, since we are working in linux land, our problem is simplified to comparing file and folder paths. We have lists of both of those things exported by [singularity-python](http://www.github.com/singularityware/singularity-python) with [these scripts](../docker). We can simplify this idea even further - each file path is like a list of sorted words. Comparing two images comes down to comparing these lists, and in this operation there are two comparisons we are interested in:

 - comparing a single file path to a second path, within the same image, or from another image
 - comparing an entire set of file paths (one image) to a (?somewhat) different set (a second image).

### Comparison of single paths
Within an image, we have some redundancy in paths that are simply longer versions of others. For example:

      ./usr/include/moar/6model',
      ./usr/include/moar/6model/reprs'

I know that the first must exist by way of the second! Thus, I might argue that it would be kind of stupid to include both of these paths in a comparison with another image. However, filtering down to a base set (for an image) is still going to require a good bit of comparison. But wait, let's remember that this is sorted, and it's sorted from simplier --> more complex paths. Here are some questions that I want to answer, to help me figure this out:

   - How many folders / files are included in each "base" image?
   - Of those included, how many are simply extensions off of a parent?

Now that I think about it, I think I have two interesting ideas for representations. If I represent an image as a graph/tree, then I can figure out if a second image is an extension of it based on it being a subgraph. I can also model the paths as being documents in a corpus, and compare corpus based on having similar documents. Maybe I'll try visualizing the graph/tree first, this might be useful to see anyway!

**STILL THINKING**


## What might the algorithm look like?

We have to have a balance of computational efficiency and accuracy. The more detailed our nitpicking the more computationally intensive, but the more computationally intensive, the less efficient. Thus, the algorithm might look something like this, to compare images A and B:

1. Break each of A and B into folders and files lists. Start with the folders:
  1. We define the number of folders in A as FoldersA and in B as FoldersB. First use the entire path as a feature (string) and do a direct comparison to find the number of strings that are exactly the same. Call them the same, and remove them from the comparison set.


# Classifying a new image into this space
Now we have some special cases, specifically, these are base images. Base images are those "official" Docker library images like Ubuntu, or Nginx, or postgres that many others are likely to build off of. There are also several ways to identify what should be a "base" image: it is likely the case that people will add on to base images, and it is less likely they will subtract from them. Thus, a base image can be found by doing the following:

- Parse a crapton of Docker files, and find the images that are most frequently used
- Logically, an image that extends some other image is a child of that image. We can build a graph/tree based on this
- We can cut the tree at some low branch to define a core set of bases.

To classify a new image into this tree space, we don't need to do pairwise comparisons of that new image with every image - we need to do graph comparisons, or start with the base sets, and then walk down the tree following the path of highest similarity. If we hit a node where the new image has fewer things than the previous base, we probably went too far. We can minimally figure out (with some confidence) where the image fits in this tree based on this algorithm, and very likely find redundancy in installation (for example, many people may extend a base image and do custom installs that are already presented in a lower branch base and thus uncessary).
