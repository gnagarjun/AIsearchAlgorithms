from Queue import Queue
import re
separator = "@#"

def bfs(source,goal,liveTraffic):
	#print 'Its bfs area'

	#BFS logic

	nodesToExplore = Queue()
	nodesToExplore.put(source)
	exploredSet=[]
	treeQueue = Queue()
	treeQueue.put(source)
	for node in iter(nodesToExplore.get,None):
		if(node == goal):
			path = treeQueue.get()
			return path
		for traffic in liveTraffic:
			#if(re.match(r"^"+node,traffic)):
			if(node == str(traffic).split(' ')[0]):
				toNode = traffic.split(' ')[1]
				if((toNode not in exploredSet) and (toNode not in nodesToExplore.queue)):
					nodesToExplore.put(toNode)
					#BFS tree construction
					edge = treeQueue.queue[0] + separator + toNode
					exploredSet.append(toNode)
					treeQueue.put(edge)
		#print "exploring node :"+node
		#exploredSet.append(node)
		treeQueue.get()

		#checking if the nodes to explore queue is empty
		if not nodesToExplore.queue:
			break


def dfs(source,goal,liveTraffic):
	#new dfs logic
	if(source == goal):
		return source
	visitedNodes = []
	#visitedNodes.append(source)
	nodesToExplore = [source,]
	
	while nodesToExplore:
		node = nodesToExplore[-1]
		nodeToexp = str(node).split(separator)[-1] 
		#print "exploring node :" + nodeToexp;
		#if(nodeToexp == goal):
		#	return node
		for traffic in reversed(liveTraffic):
			#if(re.match(r"^"+nodeToexp,traffic)):
			if(nodeToexp == str(traffic).split(' ')[0]):
				toNode = traffic.split(' ')[1]
				if(toNode == goal):
					return node + separator + toNode
				presentInQueue = False
				for qNode in nodesToExplore:
					nodeInQ = str(qNode).split(separator)[-1]
					if(nodeInQ == toNode):
						presentInqueue = True
				if((toNode not in visitedNodes) & (not presentInQueue)):
					nodesToExplore.append(node + separator + toNode)
					visitedNodes.append(toNode)
		#visitedNodes.append(nodeToexp)
		nodesToExplore.remove(node)
	#new dfs logic

def ucs(source,goal,liveTraffic):
	#print 'Its ucs area'
	import Queue as priorityQ
	nodesToExplore = priorityQ.PriorityQueue()
	nodesToExplore.put((0,0,source))
	exploredSet = []

	#ucs logic
	posPriority = 0
	for node in iter(nodesToExplore.get,None):
		nextNode = str(node[2]).split(separator)[-1]
		if(nextNode == goal):
			return [node[2],node[0]]
		
		for traffic in liveTraffic:
			#if(re.match(r"^"+nextNode,traffic)):
			if((str(traffic).split(' ')[0]) == nextNode):
				toNode = traffic.split(' ')[1]
				
				#total cost to reach the next node
				costToReach = int(traffic.split(' ')[2]) + int(node[0])

				#checking if node is in the queue already
				presentInQueue = False
				for pqNode in nodesToExplore.queue:
					nodeInQueue = (str(pqNode[2])).split(separator)[-1]
					if(nodeInQueue == toNode):
						costInQueue = pqNode[0]
						if(costInQueue > costToReach):
							nodesToExplore.queue.remove(pqNode)
						else:
							presentInQueue = True
				
				if((toNode not in exploredSet) & (not presentInQueue)):
						nodesToExplore.put((costToReach,posPriority,node[2]+separator+toNode))
						posPriority = posPriority + 1
		#print "exploirng node" + nextNode
		exploredSet.append(nextNode)

		#checking if the nodes to explore queue is empty
		if not nodesToExplore.queue:
			break
	#ucs logic


def a_star(source,goal,liveTraffic,sundayTraffic):
	#print 'Its a* area'
	#a* logic
	import Queue as priorityQ
	nodesToExplore = priorityQ.PriorityQueue()
	nodesToExplore.put([0,0,source,0])
	exploredSet = []

	posPriority = 0
	for node in iter(nodesToExplore.get,None):
		nextNode = str(node[2]).split(separator)[-1]
		if(nextNode == goal):
			return [node[2],node[3]]
		for traffic in liveTraffic:
			if((str(traffic).split(' ')[0]) == nextNode):
				toNode = traffic.split(' ')[1]
				#total cost to reach the next node
				for sundayTrafficNode in sundayTraffic:
					if(str(sundayTrafficNode).split(' ')[0] == toNode):
						toNodeHeuristic = str(sundayTrafficNode).split(' ')[1]
						break
				costTillNow = int(traffic.split(' ')[2]) + int(node[3])
				costToReach = costTillNow + int(toNodeHeuristic)

				#checking if node is in the nodesToBeExplored queue already
				presentInQueue = False
				for pqNode in nodesToExplore.queue:
					nodeInQueue = (str(pqNode[2])).split(separator)[-1]
					if(nodeInQueue == toNode):
						costInQueue = pqNode[0]
						if(costInQueue > costToReach):
							nodesToExplore.queue.remove(pqNode)
						else:
							presentInQueue = True

				#checking if node is present in exploredSet
				PresentInExploredSet = False
				for exploredNode in exploredSet:
					Enode = (str(exploredNode[2])).split(separator)[-1]
					if(Enode == toNode):
						costInExploredSet = exploredNode[0]
						if(costInExploredSet > costToReach):
							exploredSet.remove(exploredNode)
						else:
							PresentInExploredSet = True

				if((not PresentInExploredSet) & (not presentInQueue)):
					nodesToExplore.put((costToReach,posPriority,node[2]+separator+toNode,costTillNow))
					posPriority = posPriority + 1
		#print "exploring node :" + nextNode
		exploredSet.append(node)

		#checking if the nodes to explore queue is empty
		if not nodesToExplore.queue:
			break
	#a* logic


def main():
	print 'inside main area!!'

	#reading contents of the file
	fileName = 'input.txt'
	fileReader = open(fileName)
	fileContent = fileReader.read()
	fileReader.close()

	#splitting file content
	splitContent = fileContent.split('\n')
	source = splitContent[1]
	goal = splitContent[2]

	#live traffic input
	liveTrafficNumber = splitContent[3]
	liveTraffic = splitContent[4:(int(liveTrafficNumber)+4)]

	#sunday traffic info
	sundayTrafficNumberIndex = 3 + int(liveTrafficNumber) +1
	sundayTrafficNumber = splitContent[sundayTrafficNumberIndex]
	sundayTraffic = splitContent[sundayTrafficNumberIndex+1:]

	#calling respective search functions and printing output	
	if ('BFS' in splitContent) or ('bfs' in splitContent):
		path = bfs(source,goal,liveTraffic)
		bfsFileWriter = open("output.txt",'w')
		i=0
		for bfsResultNode in path.split(separator):
			bfsFileWriter.write(bfsResultNode + ' ' + str(i)+'\n')
			i = i + 1
		bfsFileWriter.close()

	if ('DFS' in splitContent) or ('dfs' in splitContent):
		visitedNodes = []
		path = dfs(source,goal,liveTraffic)
		dfsFileWriter = open("output.txt",'w')
		i=0
		for dfsResultNode in path.split(separator):
			dfsFileWriter.write(dfsResultNode + ' ' + str(i)+'\n')
			i = i + 1
		dfsFileWriter.close()

	if ('UCS' in splitContent) or ('ucs' in splitContent):
		path = ucs(source,goal,liveTraffic)
		path2 = path[0].split(separator)
		i=0
		ucsFileWriter = open("output.txt",'w')
		ucsFileWriter.write(source + ' ' + '0'+'\n')
		lenPath = len(path2) - 1
		previousCost = 0
		for i in range(0,lenPath):
			fromNode = path2[i]
			toNode = path2[i+1]
			for traffic in liveTraffic:	
				splitTraffic = str(traffic).split(' ')
				if((splitTraffic[0] == fromNode) & (splitTraffic[1] == toNode)):
					cost = int(splitTraffic[2]) + previousCost
					previousCost = cost
					break
			ucsFileWriter.write(toNode + ' ' + str(cost)+ '\n')
		ucsFileWriter.close()


	if ('A*' in splitContent) or ('a*' in splitContent):
		pathInfo = a_star(source,goal,liveTraffic,sundayTraffic)
		#print pathInfo[0]
		#print pathInfo[1]
		path2 = str(pathInfo[0]).split(separator)
		a_starFileWriter = open("output.txt",'w')
		a_starFileWriter.write(source + ' ' + '0'+'\n')
		previousCost = 0
		lenPath = len(path2) - 1
		for i in range(0,lenPath):
			fromNode = path2[i]
			toNode = path2[i+1]
			for traffic in liveTraffic:	
				splitTraffic = str(traffic).split(' ')
				if((splitTraffic[0] == fromNode) & (splitTraffic[1] == toNode)):
					cost = int(splitTraffic[2]) + previousCost
					previousCost = cost
					break
			a_starFileWriter.write(toNode + ' ' + str(cost)+'\n')
		a_starFileWriter.close()

main()