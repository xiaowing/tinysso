using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using System.Net;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;

using Newtonsoft.Json;

namespace TinySSO.Client
{
    public partial class Default : System.Web.UI.Page
    {

        private const string SSO_SESSION_USERNAME = "UserName";

        protected void Page_Load(object sender, EventArgs e)
        {
            // If session exists.
            string userName = Session[SSO_SESSION_USERNAME] as string;
            if (!string.IsNullOrEmpty(userName))
            {
                StringBuilder sb = new StringBuilder();
                sb.AppendFormat("Already signed in. The current user is {0}.", userName);
                this.lblMessage.Text = sb.ToString();
                return;
            }

            // If the current request is a redirect request from tinysso.
            if (!string.IsNullOrEmpty(Request["ticket"]))
            {
                string ticket = Request["ticket"];

                TicketValidation validate_result = ValidateTicket(ticket);
                if(validate_result != null)
                {
                    if(validate_result.valid)
                    {
                        StringBuilder sb = new StringBuilder();
                        Session[SSO_SESSION_USERNAME] = validate_result.user;

                        sb.AppendFormat("Already signed in. The current user is {0}.", validate_result.user);
                        this.lblMessage.Text = sb.ToString();
                        return;
                    }
                }
            }

            // Need login
            string rtn_url = ConfigurationManager.AppSettings["Tinysso_Test_Client"];
            rtn_url = AppendUrlWithSlash(rtn_url, "default.aspx");
            Response.Redirect(ConfigurationManager.AppSettings["Tinysso_Server_SSO_Page"] + 
                "?returnUrl=" +
                Server.UrlEncode(rtn_url));            
        }

        private TicketValidation ValidateTicket(string ticket)
        {
            string validate_url = ConfigurationManager.AppSettings["Tinysso_Server_Ticket_Validateion_API"];
            validate_url = AppendUrlWithSlash(validate_url, ticket);

            HttpWebRequest request = WebRequest.Create(validate_url) as HttpWebRequest;

            string rtn_json = string.Empty;
            TicketValidation validate_result = null;
            using (HttpWebResponse response = request.GetResponse() as HttpWebResponse)
            {
                if (response.ContentType.Equals("application/json") && 
                    (response.StatusCode.Equals(HttpStatusCode.OK)))
                {
                    StreamReader reader = new StreamReader(response.GetResponseStream());
                    rtn_json = reader.ReadToEnd();
                }
            }

            if(!string.IsNullOrEmpty(rtn_json))
            {
                validate_result = JsonConvert.DeserializeObject<TicketValidation>(rtn_json);
            }

            return validate_result;
        }

        // the result will be like "srcUrl/partialUrl"
        private string AppendUrlWithSlash(string srcUrl, string partialUrl)
        {
            if (!srcUrl.EndsWith("/"))
            {
                srcUrl += "/" + partialUrl;
            }
            else
            {
                srcUrl += partialUrl;
            }

            return srcUrl;
        }
    }

    public class TicketValidation
    {
        public bool valid { get; set; }
        public string user { get; set; }
        public string newticket { get; set; }
    }
}