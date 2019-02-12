using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Ports;
using System.Threading;
using System.Xml;
using UnityEngine;
using UnityEngine.UI;

public class MicrobitSerialInterface: MonoBehaviour {
   
    private SerialPort stream = null;
    private String m_comPort;
    private Thread mThread;
    volatile bool m_isRunning = false;

    public Text m_text;
    String m_string;

    //private Dictionary<string, int> dictionary = new Dictionary<string, int>();

    // Use this for initialization
    void Start ()
    {
        // Set the text
        m_string = "Waiting for micro:bits";

        // Get the COM port
        XmlDocument xmlDoc = new XmlDocument();

        string xml = File.ReadAllText("setup.xml");

        xmlDoc.LoadXml(xml);

        XmlNode root = xmlDoc.DocumentElement;

        XmlNode firstChildElement = root.FirstChild;

        m_comPort = root["COM"].InnerText;
        Debug.Log("COM port: " + m_comPort);

        mThread = new Thread( RunThread );
        m_isRunning = true;
        mThread.Start( this );
    }

    void RunThread(object data)
    {
        string path = "output.txt";

        var threadController = (MicrobitSerialInterface)data;

        // Open the com port e.g. "\\.\COM12"
        try
        {
            if (stream == null)
            {
                stream = new SerialPort(m_comPort, 115200);

                stream.Open();
                stream.BaseStream.Flush();

                if (stream.IsOpen)
                {
                    Debug.Log("stream.IsOpen: " + m_comPort);
                }
                else
                {
                    Debug.Log("stream.IsOpen returned false: " + m_comPort);
                }
            }
        }
        catch (Exception e)
        {
            m_string = "Could not open COM port: " + e.Message;
            Debug.Log("Could not open COM port: " + e.Message);
        }

        int checkCount = 0;

        while (threadController.m_isRunning)
        {
            Debug.Log("Thread is running");

            try
            {
                if (stream.IsOpen)
                {
                    // Read the stream
                    String value = stream.ReadLine();
                    m_string = value;

        // -------------- Let's do some parsing on the string to make it more understandable
        /*
                    // Separate this if you want
                    string[] splitArray = m_string.Split(',');

                    string from = splitArray[0];
                    string to = splitArray[1];
                    int elapsedTime = Int32.Parse( splitArray[2] );
                    string signalString = splitArray[3];
                    string colour = splitArray[4];

                    int startTime = 0;

                    // Calculate the date time for this broadcast
                    if (dictionary.ContainsKey(from))
                    {
                        int foundTime;
                        dictionary.TryGetValue(from, out foundTime);
                    }
                    else
                    {
                        dictionary.Add(from, timeStamp);
                    }
        */
                    DateTime now = System.DateTime.Now;
                    string dateAndTimeVar = now.ToString("yyyy/MM/dd HH:mm:ss");
                    //Debug.Log("COM port: " + dateAndTimeVar);

                    // Format a new string with the date time
                    m_string = dateAndTimeVar + "," + m_string;
        
                    // Write some text to a log file
                    StreamWriter writer = new StreamWriter(path, true);
                    writer.WriteLine(m_string);
                    writer.Close();

                    Debug.Log("Output: " + m_string);
                }
            }
            catch (Exception e)
            {
                Debug.Log("Could not read from COM port: " + e.Message);
            }
        }

        // If the thread wasn't closed by the UX thread 
        if (stream.IsOpen)
        {
            stream.Close();
        }
        Debug.Log("My own thread ended with " + checkCount + " iterations.");
    }
    
    private void OnDestroy()
    {
        // CLose the thread
        stream.Close();

        m_isRunning = false;

        while (mThread.IsAlive)
        {
            Thread.Sleep(1);
        }
        Debug.Log("OnDestroy");
    }

    // Update is called once per frame
    void Update ()
    {
        m_text.text = m_string;
    }
}

/*
if (!Application.isEditor)
{
     System.Diagnostics.Process.GetCurrentProcess().Kill();
}
*/