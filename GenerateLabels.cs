using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Data.SqlClient;
using UnityEngine.UI;



public class GenerateLabels : MonoBehaviour {
    
    // after the sql query is executed we will have a filled users array
    List users = new List();
    // Use this for initialization
    void Start ()
    {
        // initialize global users array
        users = ConnectToDB();
    }
	
	// Update is called once per frame
	void Update ()
    {

    }
    void OnGUI()
    {
        int i = 0;
        // create a cube for each user
        foreach (User user in users)
        {
            Rect position = new Rect(i * 20, i * 20, 100, 20);
            GUI.Label(position, user.Name);
            i++;
        }
    }

    // function to connect to the db and the users list
    List ConnectToDB()
    {
        List users = new List();
        // Build connection string
        SqlConnectionStringBuilder builder = new SqlConnectionStringBuilder();
        builder.DataSource = "powermatch.database.windows.net";
        builder.UserID = "vm-spadm";
        builder.Password = "expert@78";
        builder.InitialCatalog = "PowerMatchDB";
        try
        {
            // connect to the databases
            using (SqlConnection connection = new SqlConnection(builder.ConnectionString))
            {
                // if open then the connection is established
                connection.Open();
                Debug.Log("connection established");
                // sql command
                string sql = "SELECT MAX(u.[Name]), " +
                    "MAX(u.[AboutMe]), " +
                    "MAX(u.[UserPrincipalName]), " +
                    "string_agg(s.[Name], ', '), " +
                    "u.Id FROM [dbo].[Users] u " +
                    "inner join [dbo].[UserSkills] us " +
                    "on us.UserId = u.Id " +
                    "inner join [dbo].[Skills] s " +
                    "on us.SkillId = s.Id " +
                    "group by u.Id";
                // execute sql command
                using (SqlCommand command = new SqlCommand(sql, connection))
                {
                    // read
                    using (SqlDataReader reader = command.ExecuteReader())
                    {
                        // each line in the output
                        while (reader.Read())
                        {
                            // to avoid SqlNullValueException
                            if (!reader.IsDBNull(0)
                                & !reader.IsDBNull(1)
                                & !reader.IsDBNull(3))
                            {
                                // Skills list to be attached to each user object
                                List skills = new List();
                                // get output parameters
                                string username = reader.GetString(0);
                                string aboutString = reader.GetString(1);
                                string skillsString = reader.GetString(3);
                                // as we are getting a list of skills as 
                                // a single string delimited by comma
                                // we split the string
                                string[] skillsList = skillsString.Split(',');
                                // we now iterate through each skill to initialize our
                                // skill object and put it into skills list
                                foreach (string skillName in skillsList)
                                {
                                    // initialize a skill object with a trimmed string
                                    Skill skill = new Skill(skillName.Trim());
                                    // append to the skills array
                                    skills.Add(skill);
                                }
                                // initialize User oobject
                                User user = new User(username.Trim(), aboutString.Trim(), skills);
                                users.Add(user);
                            }
                        }
                    }
                }
            }
        }
        catch (SqlException e)
        {
            Debug.Log(e.ToString());
        }
        return users;
    }
}

// init class for skill to create an array list of skills for a user
public class Skill
{
    public string Name { get; set; }
    public Skill(string Name)
    {
        this.Name = Name;
    }
}

// init class for User (that is shown on the cube)
public class User
{
    public string Name { get; set; }
    public string About { get; set; }
    public List Skills { get; set; }

    public User(string Name, string About, List Skills)
    {
        this.Name = Name;
        this.About = About;
        this.Skills = Skills;
    }

    public override string ToString()
    {
        return "Person: " + this.Name + " About me: " + this.About;
    }
}

