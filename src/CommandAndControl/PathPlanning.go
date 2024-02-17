package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Grid dimensions
const Width = 10
const Height = 10

// Obstacles (replace with actual logic)
var obstacles = map[string]bool{
	"3,2": true,
	"5,7": true,
}

// Random point within the grid
func randomPoint() (int, int) {
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(Width), rand.Intn(Height)
}

// Nearest neighbor node in the tree
func nearestNeighbor(tree []*Node, newPoint *Node) *Node {
	var nearest *Node
	minDist := float64(Width*Height) // Initialize with large value
	for _, node := range tree {
		dist := node.distance(newPoint)
		if dist < minDist {
			nearest = node
			minDist = dist
		}
	}
	return nearest
}

// Steer towards the target point within a fixed step size
func steer(start *Node, end (int, int)) *Node {
	step := 1 // Replace with actual step size based on drone capabilities
	dx := min(max(end[0]-start.X, -step), step)
	dy := min(max(end[1]-start.Y, -step), step)
	return &Node{X: start.X + dx, Y: start.Y + dy}
}

// Check if a point is valid (within grid and not an obstacle)
func isValid(x, y int) bool {
	return x >= 0 && x < Width && y >= 0 && y < Height && !obstacles[fmt.Sprintf("%d,%d", x, y)]
}

// Builds the RRT with a maximum number of iterations
func buildRRT(start (int, int), goal (int, int), maxIterations int) []*Node {
	tree := []*Node{{X: start[0], Y: start[1]}}
	for i := 0; i < maxIterations; i++ {
		randPoint := randomPoint()
		nearest := nearestNeighbor(tree, &Node{X: randPoint[0], Y: randPoint[1]})
		newPoint := steer(nearest, goal)
		if isValid(newPoint.X, newPoint.Y) {
			tree = append(tree, newPoint)
			newPoint.Parent = nearest
			if newPoint.X == goal[0] && newPoint.Y == goal[1] {
				return tree
			}
		}
	}
	return nil
}

// Extract and print the path starting from the goal node
func extractPath(node *Node) {
	if node == nil {
		return
	}
	extractPath(node.Parent)
	fmt.Printf("(%d,%d) -> ", node.X, node.Y)
}

func main() {
	start := (0, 0)
	goal := (9, 9)
	maxIterations := 1000

	path := buildRRT(start, goal, maxIterations)
	if path != nil {
		fmt.Printf("Start: (%d,%d)\n", start[0], start[1])
		extractPath(path[len(path)-1])
		fmt.Printf("Goal: (%d,%d)\n", goal[0], goal[1])
	} else {
		fmt.Println("Path not found after", maxIterations, "iterations")
	}
}

// Node struct with basic functionality
type Node struct {
	X      int
	Y      int
	Parent *Node
}

// Distance between two nodes
func (n *Node) distance(other *Node) float64 {
	dx := float64(n.X - other.X)
	dy := float64(n.Y - other.Y)
	return math.Sqrt(dx*dx + dy*dy)
}

// Helper functions for min and max
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
