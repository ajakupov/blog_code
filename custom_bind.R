customBind <- function(dataset1, dataset2, dataset3, dataset4, dataset5) {
	combinedSet <- rbind(dataset1, dataset2, dataset3, dataset4, dataset5)
	return (list(combinedSet = combinedSet))
}
