import { Renderer2 } from "@angular/core";
import Vertex from "./vertex";
import { Subscription } from "rxjs";

export default class Edge {
    private subscriptions: Subscription[] = [];
    private line: any;

    private sourcePosition: {x: number, y: number} = {x: 0, y: 0};
    private targetPosition: {x: number, y: number} = {x: 0, y: 0};

    constructor(
        private readonly renderer: Renderer2,
        private readonly svgNativeElement: any,
        private readonly sourceVertex: Vertex,
        private readonly targetVertex: Vertex
    ) {
        this.line = this.renderer.createElement('path', 'svg');
        this.renderer.setAttribute(this.line, 'stroke', 'black');
        this.renderer.setAttribute(this.line, 'stroke-width', '2');

        // Add the line to the SVG
        this.renderer.appendChild(this.svgNativeElement, this.line);

        // Subscribe to vertex position changes to update the line
        const sub1 = this.sourceVertex.positionSubject.subscribe(({x, y}) => {
            this.sourcePosition = {x, y}
            this.updatePath(x, y)
        });
        const sub2 = this.targetVertex.positionSubject.subscribe(({x, y}) => {
            this.targetPosition = {x, y}
            this.updatePath(x, y)
        });

        this.subscriptions.push(sub1, sub2);
    }

    private updatePath(x: number, y: number): void {
        const pathData = `M${this.sourcePosition.x},${this.sourcePosition.y} L${this.targetPosition.x},${this.targetPosition.y}`;
        this.renderer.setAttribute(this.line, 'd', pathData);

        // Move Path behind Rectangles
        this.movePathToBack()
    }

    private movePathToBack(): void {
        // Get the parent of the path element (should be the same as the rectangles)
        const parent = this.renderer.parentNode(this.line);
        if (parent) {
            // Use insertBefore to move the path to the front of the parent's child nodes
            this.renderer.insertBefore(parent, this.line, parent.firstChild);
        }
    }

    // Clean up subscriptions
    public destroy(): void {
        for (const sub of this.subscriptions) {
            sub.unsubscribe();
        }
    }
}