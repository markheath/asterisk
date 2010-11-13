using System;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;

namespace Asterisk
{
    public class GameArea
    {
        private readonly Canvas canvas;
        private FrameworkElement rootVisual;
        private readonly Random random;
        public int Width { get; private set; }
        public int Height { get; private set; }
        private readonly List<Star> stars;
        private Polyline polyline;

        public GameArea(Canvas canvas)
        {
            this.canvas = canvas;
            this.stars = new List<Star>();
            this.Height = 200;
            this.Width = 300;
            this.canvas = canvas;
            this.FindRootVisual();
            this.random = new Random();
            this.RedrawScreen(0);
        }

        private void FindRootVisual()
        {
            this.rootVisual = this.canvas;
            while (this.rootVisual.Parent != null)
            {
                this.rootVisual = (FrameworkElement)this.rootVisual.Parent;
            }
        }

        private void AddLine(Point from, Point to)
        {
            var line = new Line();
            line.X1 = from.X;
            line.Y1 = from.Y;
            line.X2 = to.X;
            line.Y2 = to.Y;
            line.Stroke = new SolidColorBrush(Colors.White);
            line.StrokeThickness = 2.0;
            this.canvas.Children.Add(line);
        }

        private bool IsCollision(int x, int y)
        {
            if (y <= 0 || y >= Height)
            {
                return true;
            }
            if (x >= Width)
            {
                return !(((Height / 2 + 15) > y) && (y > (Height / 2 - 15)));
            }
            var testPoint = new Point(x, y);
            var hostPoint = this.canvas.TransformToVisual(this.rootVisual).Transform(testPoint);
            //Debug.WriteLine("Test Point: {0}, Host Point: {1}" testPoint,hostPoint))
            return CheckCollisionPoint(hostPoint, this.canvas);
        }

        private bool CheckCollisionPoint(Point point, UIElement subTree)
        {
            var hits = VisualTreeHelper.FindElementsInHostCoordinates(point, subTree);
            if (hits.Count() > 0)
            {
                Debug.WriteLine(String.Format("Test Point {0} HIT {1}", point, hits.First()));
            }
            return hits.Count() > 0;
        }

        public bool AddNewPosition(int x, int y)
        {
            this.polyline.Points.Add(new Point(x, y));
            return !this.IsCollision(x, y);
        }

        private void DrawBorders()
        {
            AddLine(new Point(0, 0), new Point(Width, 0));
            AddLine(new Point(0, Height), new Point(Width, Height));
            AddLine(new Point(Width, 0), new Point(Width, Height / 2 - 15));
            AddLine(new Point(Width, Height / 2 + 15), new Point(Width, Height));
        }

        public void RedrawScreen(int level)
        {
            this.canvas.Children.Clear();
            this.DrawBorders();

            this.stars.Clear();
            foreach (int n in Enumerable.Range(0, level * 3))
            {
                var star = new Star();
                stars.Add(star);
                Canvas.SetLeft(star, this.random.Next(10, this.Width - 10));
                Canvas.SetTop(star, this.random.Next(2, this.Height - 10));
                this.canvas.Children.Add(star);
            }

            this.polyline = new Polyline();
            this.polyline.Stroke = new SolidColorBrush(Colors.Yellow);
            this.polyline.StrokeThickness = 2.0;
            this.canvas.Children.Add(this.polyline);
        }
    }
}