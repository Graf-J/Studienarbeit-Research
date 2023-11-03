import { AfterViewInit, Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
import Graph from './graph/graph';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit {
  @ViewChild('svgGraph', { static: true}) svgGraph!: ElementRef;

  private graph!: Graph;
  
  private viewBoxHeight = 800;
  private viewBoxWidth = 600;

  private zoomFactor: number;
  private svgViewportLeft: number;
  private svgViewportTop: number;

  constructor(private readonly renderer: Renderer2) {
    this.zoomFactor = 1;
    this.svgViewportLeft = 0;
    this.svgViewportTop = 0;
  }

  ngAfterViewInit(): void {
    this.graph = new Graph(this.renderer, this.svgGraph.nativeElement);
  }

  createRect(): void {
    this.renderer.setAttribute(this.svgGraph.nativeElement, 'viewBox', `0 0 ${this.viewBoxWidth} ${this.viewBoxHeight}`)
    this.graph.addVertex()
  }

  handleMouseWheel(event: WheelEvent) {
    // Adjust the zoom factor and viewBox based on the wheel event
    const svgElement = this.svgGraph.nativeElement;
    const scaleFactor = 0.9; // Adjust this value for the desired zoom sensitivity

    if (event.deltaY < 0) {
      // Zoom in
      this.zoomFactor *= scaleFactor;
    } else {
      // Zoom out
      this.zoomFactor /= scaleFactor;
    }

    // Ensure zoom factor stays within a desired range (optional)
    this.zoomFactor = Math.max(0.1, Math.min(10, this.zoomFactor));

    // Update the viewBox to apply the zoom
    const viewBoxX = this.svgViewportLeft * this.zoomFactor;
    const viewBoxY = this.svgViewportTop * this.zoomFactor;
    this.viewBoxWidth = svgElement.clientWidth * this.zoomFactor;
    this. viewBoxHeight = svgElement.clientHeight * this.zoomFactor;
    const viewBox = `${viewBoxX} ${viewBoxY} ${this.viewBoxWidth} ${this.viewBoxHeight}`;
    this.renderer.setAttribute(svgElement, 'viewBox', viewBox);
  }
}
