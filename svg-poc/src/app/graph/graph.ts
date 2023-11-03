import { Renderer2, RendererFactory2 } from "@angular/core";
import Vertex from "./vertex";
import Edge from "./edge";

export default class Graph {
    private vertices: Vertex[] = [];
    private edges: Edge[] = [];

    constructor(
        private readonly renderer: Renderer2,
        private readonly svgNativeElement: any
    ) { }

    public addVertex(): void {
        const x = Math.floor(Math.random() * (700 - 50 + 1) + 50);
        const y = Math.floor(Math.random() * (500 - 50 + 1) + 50);

        const vertex = new Vertex(this.renderer, this.svgNativeElement, x, y, 'Hello World');
        this.vertices.push(vertex);
        vertex.render();

        if (this.vertices.length >= 2) {
            this.addEdge(this.vertices[0], this.vertices[this.vertices.length - 1])
        }
    }

    public addEdge(sourceVertex: Vertex, targetVertex: Vertex): void {
        const edge = new Edge(this.renderer, this.svgNativeElement, sourceVertex, targetVertex);
        this.edges.push(edge);
    }
}