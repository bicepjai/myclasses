package roadgraph;

public class MapEdge {
	private MapNode from;
	private MapNode to;
	private String roadName;
	private String roadType;
	private double length;
	
	public MapEdge(MapNode from, MapNode to, String roadName,
			String roadType, double length) {
		this.from = from;
		this.to = to;
		this.roadName = roadName;
		this.roadType = roadType;
		this.length = length;
	}

	public MapNode getFrom() {
		return from;
	}

	public MapNode getTo() {
		return to;
	}

	public String getRoadName() {
		return roadName;
	}

	public double getLength() {
		return length;
	}

	public String getRoadType() {
		return roadType;
	}

	public MapNode getOtherNode(MapNode node)
	{
		if (node.equals(from)) 
			return to;
		else if (node.equals(to))
			return from;
		throw new IllegalArgumentException("Looking for " +
			"a point that is not in the edge");
	}
	
	public String toString() {
		String edgeString = "("+from.getLocation().getX()+","+from.getLocation().getY()+")";
		edgeString += "("+to.getLocation().getX()+","+to.getLocation().getY()+")";
		edgeString += ": "+roadName+"("+roadType+")"+"="+length+"\n";
		return edgeString;
	}


}
