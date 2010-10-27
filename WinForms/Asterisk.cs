// Asterisk.NET
// 30 May 2003, by Mark Heath
// www.wordandspirit.co.uk

// TODO: 
// configurable speed
// about box
// help page
using System;
using System.Drawing;
using System.Windows.Forms;
using System.ComponentModel;
using System.Drawing.Imaging;
using System.Reflection;
using System.Runtime.CompilerServices;

[assembly: AssemblyTitle("Asterisk")]
[assembly: AssemblyDescription(".NET version of Asterisk")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("")]
[assembly: AssemblyProduct("Asterisk")]
[assembly: AssemblyCopyright("Mark Heath")]
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]

// Major.Minor.Build.Revision
[assembly: AssemblyVersion("0.2.0.0")]

// The following attributes specify the key for the sign of your assembly. See the
// .NET Framework documentation for more information about signing.
// This is not required, if you don't want signing let these attributes like they're.
[assembly: AssemblyDelaySign(false)]
[assembly: AssemblyKeyFile("")]

public class MainForm : Form {
	[STAThread]
	public static void Main() {
		Application.Run(new MainForm());	
	}
	
	private Button twoPlayer;
	private Button newGame;
	private Timer timer;
	private Rectangle rectMain;
	private Bitmap bmpMain;
	private Label instructions1;
	private Label instructions2;
	private Label record;
	private Label level;
	private Font fnt;
	private Random rand;
	
	private int nLevel;
	private int nXPos;
	private int nYPos1;
	private int nYPos2;
	private bool blnKeyDown1;
	private bool blnKeyDown2;
	private int nRecordLevel;
	private string recordName;
	private int nPlayers;
	private Color col1 = Color.Yellow;
	private Color col2 = Color.LightGreen;

	public MainForm() {
		this.BackColor = Color.Black;
		this.Text = "Asterisk";
		this.ClientSize = new Size(320,295);
		this.Icon = new Icon(GetType().Module.Assembly.GetManifestResourceStream("asterisk.ico"));
		this.KeyPreview = true;
		
		// row 1
		level = new Label();
		level.Text = "Level 1";
		level.BackColor = Color.Black;
		level.ForeColor = Color.White;
		level.Location = new Point(10,10);
		level.Size = new Size(100,20);
		this.Controls.Add(level);

		record = new Label();
		record.Text = "Record:";
		record.BackColor = Color.Black;
		record.ForeColor = Color.White;
		record.Location = new Point(120,10);
		record.Size = new Size(190,20);
		this.Controls.Add(record);
		
		// row 2
		instructions1 = new Label();
		instructions1.Text = "Player 1: CTRL key";
		instructions1.BackColor = Color.Black;
		instructions1.ForeColor = col1;
		instructions1.Location = new Point(10,30);
		instructions1.Size = new Size(150,20);
		this.Controls.Add(instructions1);

		instructions2 = new Label();
		instructions2.Text = "Player 2: SHIFT key";
		instructions2.BackColor = Color.Black;
		instructions2.ForeColor = col2;
		instructions2.Location = new Point(165,30);
		instructions2.Size = new Size(150,20);
		this.Controls.Add(instructions2);

		// row 3
		rectMain = new Rectangle(new Point(10,55),new Size(300,200));
		bmpMain = new Bitmap(300,200,PixelFormat.Format24bppRgb);
		
		// row 4
		newGame = new Button();
		newGame.Text = "&1 Player";
		newGame.Location = new Point(30,265);
		newGame.Click += new EventHandler(OnNewGame);
		newGame.BackColor = Color.LightGray;
		this.Controls.Add(newGame);

		twoPlayer = new Button();
		twoPlayer.Text = "&2 Player";
		twoPlayer.Location = new Point(185,265);
		twoPlayer.Click += new EventHandler(OnTwoPlayer);
		twoPlayer.BackColor = Color.LightGray;
		this.Controls.Add(twoPlayer);

		timer = new Timer();
		timer.Tick += new EventHandler(OnTimerTick);
		timer.Interval = 20; // milliseconds
		
		fnt = new Font("Courier New",12,FontStyle.Bold);
		rand = new Random();
		this.AcceptButton = newGame;

		nRecordLevel = (int) Application.UserAppDataRegistry.GetValue("Level",(int) 1);
		recordName = (string) Application.UserAppDataRegistry.GetValue("Name","nobody");
	   	
	   	ShowRecord();
	   	// just to redraw screen
	   	NewLevel();
	}

	// New Game button clicked
	private void OnNewGame(object sender, EventArgs e) {
	   nPlayers = 1;
	   NewGame();
	}

	// 2 player button clicked
	private void OnTwoPlayer(object sender, EventArgs e) {
		nPlayers = 2;
		NewGame();
	}

	// start a new game
	private void NewGame() {
	   newGame.Enabled = false;
	   twoPlayer.Enabled = false;
	   nLevel = 0;
	   NewLevel();
	   timer.Start();
	}
	
	// check for control or shift key pressed
	protected override void OnKeyDown(KeyEventArgs e) {
		if(e.KeyCode == Keys.ControlKey) {
			blnKeyDown1 = true;
		}
		else if(e.KeyCode == Keys.ShiftKey) {
			blnKeyDown2 = true;
		}
		base.OnKeyDown(e);
	}

	// check for control or shift key released
	protected override void OnKeyUp(KeyEventArgs e) {
		if(e.KeyCode == Keys.ControlKey) {
			blnKeyDown1 = false;
		}
		else if(e.KeyCode == Keys.ShiftKey) {
			blnKeyDown2 = false;
		}
		base.OnKeyUp(e);
	}


	// paints the new level onto the global bitmap, and then invalidates the relevant part of the screen
	private void RedrawScreen() {
		int nAsterisks;
        
        Graphics g = Graphics.FromImage(bmpMain);
		Pen whitePen = new Pen(Color.White);
		g.FillRectangle(new SolidBrush(Color.Black),0,0,rectMain.Width,rectMain.Height);
		g.DrawLine(whitePen,new Point(0,0),new Point(rectMain.Width - 1,0));
		g.DrawLine(whitePen,new Point(0,rectMain.Height - 1),new Point(rectMain.Width, rectMain.Height - 1));
		g.DrawLine(whitePen,new Point(rectMain.Width - 1, 0),new Point(rectMain.Width - 1, rectMain.Height - 1));
		g.DrawLine(new Pen(Color.Black),new Point(rectMain.Width - 1, 15 + rectMain.Height / 2),new Point(rectMain.Width - 1, (rectMain.Height / 2) - 15) );

		nAsterisks = nLevel * 3;
		for(int n = 0; n < nAsterisks; n++) {
			g.DrawString("*",fnt,new SolidBrush(Color.White),new Point(rand.Next(10, rectMain.Width - 10),rand.Next(0, rectMain.Height - 10)));
		}
	
		this.Invalidate(rectMain);
		g.Dispose();
		
	}

	// stop the game when the application closes
	protected override void OnClosing(CancelEventArgs e) {
	   	timer.Stop();
		base.OnClosing(e);
	}
	
	// move the position on one
	private void OnTimerTick(object sender, EventArgs e) {
		nXPos++;
		if(blnKeyDown1) {
			nYPos1--;
		}
		else {
			nYPos1++;
		}
		if(blnKeyDown2) {
			nYPos2--;
		}
		else {
			nYPos2++;
		}
		CheckPosition();
		
		bmpMain.SetPixel(nXPos,nYPos1,col1);
		this.Invalidate(new Rectangle(rectMain.X + nXPos,rectMain.Y + nYPos1,1,1));
		if(nPlayers > 1) {
			bmpMain.SetPixel(nXPos,nYPos2,col2);
			this.Invalidate(new Rectangle(rectMain.X + nXPos,rectMain.Y + nYPos2,1,1));
		}
		
	}
	
	// check that we have not crashed by seeing if the pixel we are about to fill in is white or not
	// note that to compare a pixel to a 'named color' you need to use ToArgb() 
	private void CheckPosition() {
		bool blnPlayer1Crash = false;
		bool blnPlayer2Crash = false;
		
		if(nXPos >= rectMain.Width) {
			NewLevel();
			return;
		}
			
		// n.b. not all the pixels are white as the DrawString function emits greyscale for smooth edges
		if(bmpMain.GetPixel(nXPos, nYPos1).ToArgb() != Color.Black.ToArgb()) { 
			blnPlayer1Crash = true;
		}
		if(nPlayers > 1) {
			if(bmpMain.GetPixel(nXPos, nYPos2).ToArgb() != Color.Black.ToArgb()) {
				blnPlayer2Crash = true;
			}
		}
		
		
		if(blnPlayer1Crash || blnPlayer2Crash) {
			timer.Stop();
			if(nPlayers == 1) {
				if(nLevel > nRecordLevel) {
					InputStringDialog dlg = new InputStringDialog("High Score! Enter your name:",recordName,20);
					dlg.ShowDialog();
					recordName = dlg.UserInput;
					nRecordLevel = nLevel;
					ShowRecord();
				}
				else {
					MessageBox.Show("Game Over");
				}			
				newGame.Enabled = true;
				twoPlayer.Enabled = true;
			}
			else {
				string message;
				if(blnPlayer1Crash && blnPlayer2Crash) {
					message = "Draw, play again?";	
				}
				else if(blnPlayer1Crash) {
					message = "Player 2 wins, play again?";
				}
				else {
					message = "Player 1 wins, play again?";
				}
				
				if(MessageBox.Show(message,Application.ProductName,MessageBoxButtons.YesNo) == DialogResult.Yes) {
					OnTwoPlayer(null,null);
				}
				else {
					newGame.Enabled = true;
					twoPlayer.Enabled = true;
				}
			}
		}
	}
	
	// reset variables ready for the next level
	private void NewLevel() {
	   nLevel = nLevel + 1;
	   nXPos = 0;
	   if(nPlayers == 1) {
		  nYPos1 = rectMain.Height / 2;
	   }
	   else {
		  nYPos1 = rectMain.Height / 4;
		  nYPos2 = (3 * rectMain.Height) / 4;
	   }
	   level.Text = String.Format("Level {0}",nLevel);
	   blnKeyDown1 = false;
	   blnKeyDown2 = false;
	   RedrawScreen();
	}

	// save the current record in the registry and update the label
	private void ShowRecord() {
		Application.UserAppDataRegistry.SetValue("Level",nRecordLevel);
		Application.UserAppDataRegistry.SetValue("Name",recordName);
		record.Text = String.Format("Record: Level {0} by {1}",nRecordLevel,recordName);
	}
	
	// paints the bitmap onto the screen
	// to avoid flicker, we only paint the contents of the invalid rectangle
	// TODO: we should really check that the invalid rectangle is just the client area (although it doesn't seem to cause problems)
	protected override void OnPaint(PaintEventArgs e) {
		Graphics g = e.Graphics;
		//g.DrawImage(bmpMain, rectMain);
		
		Rectangle src = new Rectangle(e.ClipRectangle.X - rectMain.X,e.ClipRectangle.Y - rectMain.Y,e.ClipRectangle.Width,e.ClipRectangle.Height);
		g.DrawImage(bmpMain,e.ClipRectangle,src,GraphicsUnit.Pixel);
	}
}


// simple replacement class for the old VB InputBox function
public class InputStringDialog : Form {
	private TextBox txt;
	private Button ok;
	private Label lblPrompt;
	private string userInput;
	
	public string UserInput {
		get {
			return userInput;
		}
	}
	
	public InputStringDialog(string prompt,string defaultValue, int maxChars) {
		int textWidth = 290;
		this.Text = Application.ProductName;
		
		this.ClientSize = new Size(textWidth + 10,80);
		this.MinimumSize = this.Size;
		
		lblPrompt = new Label();
		lblPrompt.Location = new Point(5,5);
		lblPrompt.Size = new Size(textWidth,15);
		lblPrompt.Text = prompt;
		lblPrompt.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
		this.Controls.Add(lblPrompt);
				
		txt = new TextBox();
		txt.Location = new Point(5,25);
		txt.Size = new Size(textWidth,20);
		txt.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
		txt.Text = defaultValue;
		txt.MaxLength = maxChars;
		this.Controls.Add(txt);
		
		ok = new Button();
		ok.Location = new Point(ClientSize.Width - 85,50);
		ok.Size = new Size(60,25);
		ok.Anchor = AnchorStyles.Right | AnchorStyles.Bottom;
		ok.Text = "OK";
		ok.Click += new EventHandler(OnOK);
		this.Controls.Add(ok);
		
		this.AcceptButton = ok;
		userInput = defaultValue;
	}
	
	private void OnOK(object sender, EventArgs ea) {
		userInput = txt.Text;
		this.Close();
	}
}