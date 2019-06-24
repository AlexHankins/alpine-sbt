#!/usr/bin/env python

def main():
	versionStrs = []
	try:
		fd = open('sbt-versions.txt')
		versionStrs = loadVersionsFromFile(fd)
	finally:
		fd.close()

	aliasToVersionMap = buildAliasToVersionMap(versionStrs)

	try:
		fd = open('README.md', 'w')
		generateReadMe(aliasToVersionMap, versionStrs, fd)
	finally:
		fd.close()

def assignAliasIfNotAlreadyPresent(
		alias,
		version,
		aliasToVersionMap,
		tagDescription=None
	):
	if alias not in aliasToVersionMap.keys():
		if tagDescription is None:
			tagDescription = 'latest sbt version %s.x' % (
				alias)
		# assign alias to that version
		print("git tag -m '%s' '%s' '%s'" % (
			tagDescription,
			alias,
			version,
		))
		aliasToVersionMap[alias] = version

def buildAliasToVersionMap(versionStrs):
	aliasToVersionMap = {}

	for version in versionStrs:
		# array of [major, minor, bugfix]
		mamibu = version.split('.')

		assignAliasIfNotAlreadyPresent(
			mamibu[0],
			version,
			aliasToVersionMap,
		)

		assignAliasIfNotAlreadyPresent(
			mamibu[0] + '.' + mamibu[1],
			version,
			aliasToVersionMap,
		)

	# Assign "latest" tag to highest version
	assignAliasIfNotAlreadyPresent('latest',
		versionStrs[0],
		aliasToVersionMap,
		'Latest stable sbt version.')

	return aliasToVersionMap


def generateReadMe(aliasToVersionMap, versionStrs, readMeFile):
	repoPrefix = 'https://github.com/AlexHankins/alpine-sbt/blob/'
	# + '<tag>/Dockerfile'

	#print(":aliasToVersionMap = %s" % (repr(aliasToVersionMap,)))
	#print(":aliases for 1.2.8 = %s" % (repr(getAliases('1.2.8', aliasToVersionMap))))

	readmeFile.write("""
	# Supported tags and respective `Dockerfile` links

	""")

	for version in versionStrs:
		readmeFile.write("* [%s](%s)\n" % (
			toCommaSeparateMarkdownLiterals(getAliases(version, aliasToVersionMap))
			,repoPrefix + version + '/Dockerfile'))


	# @TODO add directions `# How to use this image` at some point...

# always returns a list of at least one item
def getAliases(version, aliasToVersionMap):
	res = [version]
	for alias, thatVersion in aliasToVersionMap.items():
		if thatVersion == version:
			res.append(alias)
	return res

plus = lambda (x,y): x + y

def loadVersionsFromFile(fd):
	versionStrs = [x.strip() for x in fd.readlines()]
	versionStrs.sort()
	versionStrs.reverse()
	return versionStrs

# returns string
def toCommaSeparateMarkdownLiterals(ls):
	markdowns = ['`' + elt + '`, ' for elt in ls]
	cats = reduce(plus, markdowns)
	return cats[:-2]  # strip trailing ", "


main()
