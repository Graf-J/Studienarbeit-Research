import { Renderer2 } from "@angular/core";
import { BehaviorSubject } from "rxjs";

export default class Vertex {
    public positionSubject: BehaviorSubject<{x: number, y: number}>;

    private group: any;
    private text: any;
    private rect: any;

    private isDragging: boolean = false;
    private initialMouseX: number;
    private initialMouseY: number;
    private initialX: number;
    private initialY: number;

    constructor(
        private readonly renderer: Renderer2,
        private readonly svgNativeElement: any,
        public x: number, 
        public y: number,
        private label: string = '',
        private color: string = 'lightblue',
    ) { 
        this.positionSubject = new BehaviorSubject({x, y});
        this.group = this.renderer.createElement('g', 'svg');
        this.text = this.renderer.createElement('text', 'svg');
        this.rect = this.renderer.createElement('rect', 'svg');
        this.isDragging = false;
        this.initialMouseX = 0;
        this.initialMouseY = 0;
        this.initialX = 0;
        this.initialY = 0;
    }

    public render(): void {
        // Create the <g> element for grouping
        this.group = this.renderer.createElement('g', 'svg');

        // Create the <text> element for the label
        this.text = this.renderer.createElement('text', 'svg');
        this.renderer.setAttribute(this.text, 'x', (this.x + 50).toString()); // Position in the middle of the rect
        this.renderer.setAttribute(this.text, 'y', (this.y + 25).toString()); // Position in the middle of the rect
        this.renderer.setAttribute(this.text, 'text-anchor', 'middle'); // Center text horizontally
        this.renderer.setAttribute(this.text, 'dominant-baseline', 'middle'); // Center text vertically
        const textContent = this.renderer.createText('Hello World'); // Replace with your desired text
        this.renderer.appendChild(this.text, textContent);
        // Initialize first value for Subject
        this.positionSubject.next({x: this.x + 50, y: this.y + 25});

        // Create the <rect> element
        this.rect = this.renderer.createElement('rect', 'svg');
        this.renderer.setAttribute(this.rect, 'x', this.x.toString());
        this.renderer.setAttribute(this.rect, 'y', this.y.toString());
        this.renderer.setAttribute(this.rect, 'width', '100');
        this.renderer.setAttribute(this.rect, 'height', '50');
        this.renderer.setAttribute(this.rect, 'fill', this.color);

        // Add mouse event listeners for dragging
        this.renderer.listen(this.group, 'mousedown', (event: MouseEvent) => this.onMouseDown(event));
        this.renderer.listen(document, 'mousemove', (event: MouseEvent) => this.onMouseMove(event));
        this.renderer.listen(this.group, 'mouseup', () => this.onMouseUp());

        // Append both the <rect> and <text> elements to the <g>
        this.renderer.appendChild(this.group, this.rect);
        this.renderer.appendChild(this.group, this.text);

        // Append the <g> to the SVG
        this.renderer.appendChild(this.svgNativeElement, this.group);
    }

    private onMouseDown(event: MouseEvent): void {
        event.stopPropagation();
        this.isDragging = true;

        // Normalize the initial mouse coordinates
        const normalizedMouse = this.normalizeMouseCoordinates(event);
        this.initialMouseX = normalizedMouse.x;
        this.initialMouseY = normalizedMouse.y;

        this.initialX = this.x;
        this.initialY = this.y;
    }

    private onMouseMove(event: MouseEvent): void {
        if (this.isDragging) {
            // Normalize the current mouse coordinates
            const normalizedMouse = this.normalizeMouseCoordinates(event);
            const normalizedX = normalizedMouse.x;
            const normalizedY = normalizedMouse.y;
    
            // Calculate the delta based on the normalized coordinates
            const deltaX = normalizedX - this.initialMouseX;
            const deltaY = normalizedY - this.initialMouseY;
    
            // Update the position in the content coordinates
            this.x = this.initialX + deltaX;
            this.y = this.initialY + deltaY;
    
            // Update the position of the SVG element based on the content coordinates
            this.updatePosition();
        }
    }

    private onMouseUp(): void {
        this.isDragging = false;
    }

    private updatePosition(): void {
        this.renderer.setAttribute(this.rect, 'x', this.x.toString());
        this.renderer.setAttribute(this.rect, 'y', this.y.toString());
        this.renderer.setAttribute(this.text, 'x', (this.x + 50).toString());
        this.renderer.setAttribute(this.text, 'y', (this.y + 25).toString());
        this.positionSubject.next({ x: this.x + 50, y: this.y + 25 })
    }

    private normalizeMouseCoordinates(event: MouseEvent): { x: number; y: number } {
        const svgElement = this.svgNativeElement;
        const svgCTM = svgElement.getScreenCTM().inverse();
        const mouseX = event.clientX;
        const mouseY = event.clientY;
    
        // Normalize the mouse coordinates using the viewBox and zoom factor
        let normalizedMouse = svgElement.createSVGPoint();
        normalizedMouse.x = mouseX;
        normalizedMouse.y = mouseY;
        normalizedMouse = normalizedMouse.matrixTransform(svgCTM);
    
        return { x: normalizedMouse.x, y: normalizedMouse.y };
    }
}