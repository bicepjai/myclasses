/**
 * @author UCSD MOOC development team and YOU
 * 
 * A class which reprsents a graph of geographic locations
 * Nodes in the graph are intersections between 
 *
 */
package roadgraph;


import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Set;
import java.util.function.Consumer;
import java.util.Comparator;

import geography.GeographicPoint;
import util.GraphLoader;

/**
 * @author UCSD MOOC development team and YOU
 * 
 * A class which represents a graph of geographic locations
 * Nodes in the graph are intersections between 
 *
 */
public class MapGraph {


	private HashMap<GeographicPoint,MapNode> vertices;
	
	/** 
	 * Create a new empty MapGraph 
	 */
	public MapGraph()
	{
		// TODO: Implement in this constructor in WEEK 2
		vertices = new HashMap<GeographicPoint,MapNode>();
	}
	
	/**
	 * Get the number of vertices (road intersections) in the graph
	 * @return The number of vertices in the graph.
	 */
	public int getNumVertices()
	{
		//TODO: Implement this method in WEEK 2
		return vertices.size();
	}
	
	/**
	 * Return the intersections, which are the vertices in this graph.
	 * @return The vertices in this graph as GeographicPoints
	 */
	public Set<GeographicPoint> getVertices()
	{
		//TODO: Implement this method in WEEK 2
		return vertices.keySet();
	}
	
	/**
	 * Get the number of road segments in the graph
	 * @return The number of edges in the graph.
	 */
	public int getNumEdges()
	{
		//TODO: Implement this method in WEEK 2
		int numEdges = 0;
		for (GeographicPoint node : vertices.keySet()) {
			numEdges += vertices.get(node).getNeighbors().size();
		}
		return numEdges;
	}

	
	
	/** Add a node corresponding to an intersection at a Geographic Point
	 * If the location is already in the graph or null, this method does 
	 * not change the graph.
	 * @param location  The location of the intersection
	 * @return true if a node was added, false if it was not (the node
	 * was already in the graph, or the parameter is null).
	 */
	public boolean addVertex(GeographicPoint location)
	{
		// TODO: Implement this method in WEEK 2
		if(location == null) {
			return false;
		}
		if(vertices.containsKey(location)) {
			return false;
		}
		MapNode vertex = new MapNode(location);
		vertices.put(location, vertex);
		return false;
	}
	
	/**
	 * Adds a directed edge to the graph from pt1 to pt2.  
	 * Precondition: Both GeographicPoints have already been added to the graph
	 * @param from The starting point of the edge
	 * @param to The ending point of the edge
	 * @param roadName The name of the road
	 * @param roadType The type of the road
	 * @param length The length of the road, in km
	 * @throws IllegalArgumentException If the points have not already been
	 *   added as nodes to the graph, if any of the arguments is null,
	 *   or if the length is less than 0.
	 */
	public void addEdge(GeographicPoint from, GeographicPoint to, String roadName,
			String roadType, double length) throws IllegalArgumentException {

		//TODO: Implement this method in WEEK 2
		addVertex(from);
		addVertex(to);
		MapNode fromNode = vertices.get(from);
		MapNode toNode = vertices.get(to);
		MapEdge edge = new MapEdge(fromNode, toNode, roadName, roadType, length);
		System.out.println(edge.toString());
		vertices.get(from).addEdge(edge);
	}
	

	/** Find the path from start to goal using breadth first search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest (unweighted)
	 *   path from start to goal (including both start and goal).
	 */
	public List<GeographicPoint> bfs(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
        Consumer<GeographicPoint> temp = (x) -> {};
        return bfs(start, goal, temp);
	}
	
	/** Find the path from start to goal using breadth first search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest (unweighted)
	 *   path from start to goal (including both start and goal).
	 */
	public List<GeographicPoint> bfs(GeographicPoint start, 
			 					     GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		// TODO: Implement this method in WEEK 2
		
		// Hook for visualization.  See writeup.
		//nodeSearched.accept(next.getLocation());

		if (start == null || goal == null) {
			System.out.println("Start or goal node is null!  No path exists.");
			return new LinkedList<GeographicPoint>();
		}
		
		MapNode startNode = vertices.get(start);
		MapNode goalNode = vertices.get(goal);
		
		if (startNode == null) {
			System.err.println("Start node " + start + " does not exist");
			return null;
		}
		if (goalNode == null) {
			System.err.println("End node " + goal + " does not exist");
			return null;
		}
		
		Queue<MapNode> toExplore = new LinkedList<MapNode>();
		HashMap<MapNode, MapNode> parentMap = new HashMap<MapNode, MapNode>();
		HashSet<MapNode> visited = new HashSet<MapNode>();
		toExplore.add(startNode);
		MapNode curr = null;
		while (!toExplore.isEmpty()) {
			curr = toExplore.remove();
			
			// Hook for visualization.
			nodeSearched.accept(curr.getLocation());
			
			if (curr.equals(goalNode)) {
				break;
			}
			
			Set<MapNode> neighbors = curr.getNeighbors();
			for (MapNode neighbor : neighbors) {
				if (!visited.contains(neighbor)) {
					visited.add(neighbor);
					parentMap.put(neighbor, curr);
					toExplore.add(neighbor);
				}
			}
		}

		if (!curr.equals(goalNode)) {
			System.out.println("BFS: No path found from " +start+ " to " + goal);
			return null;
		}
		
		List<GeographicPoint> path = reconstructPath(parentMap, startNode, goalNode);
		return path;
	}


	private List<GeographicPoint>
	reconstructPath(HashMap<MapNode,MapNode> parentMap,
					MapNode start, MapNode goal)
	{
		LinkedList<GeographicPoint> path = new LinkedList<GeographicPoint>();
		MapNode current = goal;

		while (!current.equals(start)) {
			path.addFirst(current.getLocation());
			current = parentMap.get(current);
		}

		// add start
		path.addFirst(start.getLocation());
		return path;
	}
	
	/** Find the path from start to goal using Dijkstra's algorithm
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> dijkstra(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
		// You do not need to change this method.
        Consumer<GeographicPoint> temp = (x) -> {};
        return dijkstra(start, goal, temp);
	}
	
	/** Find the path from start to goal using Dijkstra's algorithm
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> dijkstra(GeographicPoint start, 
										  GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		
		if (start == null || goal == null) {
			System.out.println("Start or goal node is null!  No path exists.");
			return new LinkedList<GeographicPoint>();
		}

		if (!vertices.containsKey(start) || !vertices.containsKey(goal)) {
			System.out.println("Start or goal node is not present in map!  No path exists.");
			return new LinkedList<GeographicPoint>();
		}
		
		MapNode startNode = vertices.get(start);
		MapNode goalNode = vertices.get(goal);
		
		PriorityQueue<MapNode> toExplore = new PriorityQueue<MapNode>(1, new Comparator<MapNode>() {
	        public int compare(MapNode node1, MapNode node2) {
	            return node1.compareBackwardDistance(node2);
	        }
		});
		HashMap<MapNode, MapNode> parentMap = new HashMap<MapNode, MapNode>();
		HashSet<MapNode> visited = new HashSet<MapNode>();
		toExplore.add(startNode);
		startNode.setBackwardDistance(0.0);
		MapNode curr = null;
		while (!toExplore.isEmpty()) {
			curr = toExplore.remove();
			
			// Hook for visualization.
			nodeSearched.accept(curr.getLocation());
			
			if (!visited.contains(curr)) {
				visited.add(curr);
				
				if (curr.equals(goalNode)) {
					break;
				}
				
				Set<MapNode> neighbors = curr.getNeighbors();
				for (MapNode neighbor : neighbors) {
					if (!visited.contains(neighbor)) {
						double currDistance = curr.getBackwardDistance() + neighbor.getDistanceFrom(curr);
						if( currDistance < neighbor.getBackwardDistance())
						{
							neighbor.setBackwardDistance(currDistance);
							parentMap.put(neighbor, curr);
							toExplore.add(neighbor);
						}
					}
				}
			}
		}

		if (!curr.equals(goalNode)) {
			System.out.println("DIJIKSTRA: No path found from " +start+ " to " + goal);
			return null;
		}
		
		List<GeographicPoint> path = reconstructPath(parentMap, startNode, goalNode);
		return path;
	}

	/** Find the path from start to goal using A-Star search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> aStarSearch(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
        Consumer<GeographicPoint> temp = (x) -> {};
        return aStarSearch(start, goal, temp);
	}
	
	/** Find the path from start to goal using A-Star search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> aStarSearch(GeographicPoint start, 
											 GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		
		if (start == null || goal == null) {
			System.out.println("Start or goal node is null!  No path exists.");
			return new LinkedList<GeographicPoint>();
		}

		if (!vertices.containsKey(start) || !vertices.containsKey(goal)) {
			System.out.println("Start or goal node is not present in map!  No path exists.");
			return new LinkedList<GeographicPoint>();
		}
		
		MapNode startNode = vertices.get(start);
		MapNode goalNode = vertices.get(goal);
		
		PriorityQueue<MapNode> toExplore = new PriorityQueue<MapNode>(1, new Comparator<MapNode>() {
	        public int compare(MapNode node1, MapNode node2) {
	            return node1.comparePredictedDistance(node2);
	        }
		});
		HashMap<MapNode, MapNode> parentMap = new HashMap<MapNode, MapNode>();
		HashSet<MapNode> visited = new HashSet<MapNode>();
		toExplore.add(startNode);
		startNode.setBackwardDistance(0.0);
		startNode.setPredictedForwardDistance(0.0);
		MapNode curr = null;
		while (!toExplore.isEmpty()) {
			curr = toExplore.remove();
			
			// Hook for visualization.
			nodeSearched.accept(curr.getLocation());
			
			if (!visited.contains(curr)) {
				visited.add(curr);
				
				if (curr.equals(goalNode)) {
					break;
				}
				
				Set<MapNode> neighbors = curr.getNeighbors();
				for (MapNode neighbor : neighbors) {
					if (!visited.contains(neighbor)) {
						double predictedDistance = curr.getBackwardDistance() + neighbor.getDistanceFrom(curr) + neighbor.getDistanceFrom(goalNode);
						if( predictedDistance < neighbor.getPredictedForwardDistance())
						{
							neighbor.setBackwardDistance(curr.getBackwardDistance() + neighbor.getDistanceFrom(curr));
							neighbor.setPredictedForwardDistance(predictedDistance);
							parentMap.put(neighbor, curr);
							toExplore.add(neighbor);
						}
					}
				}
			}
		}

		if (!curr.equals(goalNode)) {
			System.out.println("ASTAR: No path found from " +start+ " to " + goal);
			return null;
		}
		
		List<GeographicPoint> path = reconstructPath(parentMap, startNode, goalNode);
		return path;
	}

	
	
	public static void main(String[] args)
	{
//		GraphLoader.createIntersectionsFile("data/graders/mod3/map3.txt", "data/intersections/map3.intersections");
		
		System.out.print("Making a new map...");
		MapGraph theMap = new MapGraph();
		System.out.print("DONE. \nLoading the map...\n");

//		GraphLoader.loadRoadMap("data/testdata/simpletest.map", theMap);
//		GeographicPoint start = new GeographicPoint(7, 3);
//		GeographicPoint end = new GeographicPoint(4, -1);
//		GeographicPoint start = new GeographicPoint(1.0, 1.0);
//		GeographicPoint end = new GeographicPoint(8.0, -1.0);
		
		GraphLoader.loadRoadMap("data/graders/mod3/map3.txt", theMap);
		GeographicPoint start = new GeographicPoint(0.0, 0.0);
		GeographicPoint end = new GeographicPoint(0.0, 4.0);
		
//		GraphLoader.loadRoadMap("data/maps/utc.map", theMap);
//		GeographicPoint start = new GeographicPoint(32.8648772, -117.2254046);
//		GeographicPoint end = new GeographicPoint(32.8660691, -117.217393);

		System.out.println("DONE.");
		

		System.out.println("Num nodes: " + theMap.getNumVertices());
		System.out.println("Num edges: " + theMap.getNumEdges());
	
		System.out.println("\n BFS");
		List<GeographicPoint> route1 = theMap.bfs(start, end);
		for (GeographicPoint intersection : route1) {
			System.out.println(intersection.getX() + " " + intersection.getY());
		}
		
		System.out.println("\n DIJIKSTRA");
		List<GeographicPoint> route2 = theMap.dijkstra(start,end);
		for (GeographicPoint intersection : route2) {
			System.out.println(intersection.getX() + " " + intersection.getY());
		}
		
		System.out.println("\n ASTAR");
		List<GeographicPoint> route3 = theMap.aStarSearch(start,end);
		for (GeographicPoint intersection : route3) {
			System.out.println(intersection.getX() + " " + intersection.getY());
		}
		
	}
	
}
