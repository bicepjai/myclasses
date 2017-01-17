package roadgraph;

import java.util.HashSet;
import java.util.Set;

import geography.GeographicPoint;

public class MapNode {
	
	private GeographicPoint location;
	private HashSet <MapEdge> edges;
	private double predictedForwardDistance;
	private double backwardDistance;

	public MapNode(GeographicPoint location) {
		this.location = location;
		edges = new HashSet<MapEdge>();
		setPredictedForwardDistance(Double.POSITIVE_INFINITY);
		backwardDistance = Double.POSITIVE_INFINITY;
	}
	
	GeographicPoint getLocation() {
		return this.location;
	}
	
	void addEdge(MapEdge edge) {
		this.edges.add(edge);
	}

	public int HashCode()
	{
		return location.hashCode();
	}

	public boolean equals(Object o)
	{
		if (!(o instanceof MapNode) || (o == null)) {
			return false;
		}
		MapNode node = (MapNode)o;
		return node.location.equals(this.location);
	}
	
	Set<MapNode> getNeighbors()
	{
		Set<MapNode> neighbors = new HashSet<MapNode>();
		for (MapEdge edge : edges) {
			neighbors.add(edge.getOtherNode(this));
		}
		return neighbors;
	}
	
	public String toString() {
		String nodeName = location.toString();
		for (MapEdge edge : edges) {
			nodeName += edge.toString();
			nodeName += new String("\t");
		}
		return nodeName;
	}

    // Code to implement Comparable
	public int compareBackwardDistance(MapNode other) {
		return ((Double)this.getBackwardDistance()).compareTo((Double) other.getBackwardDistance());
	}

    // Code to implement Comparable
	public int comparePredictedDistance(MapNode other) {
		return ((Double)this.getPredictedForwardDistance())
				.compareTo((Double)other.getPredictedForwardDistance());
	}
	
	public double getDistanceFrom(MapNode other) {
		return this.getLocation().distance(other.getLocation());
	}

	public double getBackwardDistance() {
		return backwardDistance;
	}

	public void setBackwardDistance(double backwardDistance) {
		this.backwardDistance = backwardDistance;
	}

	public double getPredictedForwardDistance() {
		return predictedForwardDistance;
	}

	public void setPredictedForwardDistance(double predictedForwardDistance) {
		this.predictedForwardDistance = predictedForwardDistance;
	}
}
