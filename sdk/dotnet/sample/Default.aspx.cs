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

using Tinysso.Client;
using Newtonsoft.Json;

namespace TinySSO.Client
{
    public partial class Default : System.Web.UI.Page
    {

        private const string SSO_SESSION_USERNAME = "UserName";
        private Executor executor = null; 

        protected void Page_Load(object sender, EventArgs e)
        {
            string rtn_url = ConfigurationManager.AppSettings["Tinysso_Client"];
            string sso_url = ConfigurationManager.AppSettings["Tinysso_Server"];

            // If session exists.
            string userName = Session[SSO_SESSION_USERNAME] as string;
            if (!string.IsNullOrEmpty(userName))
            {
                StringBuilder sb = new StringBuilder();
                sb.AppendFormat("Already signed in. The current user is {0}.", userName);
                this.lblMessage.Text = sb.ToString();
                return;
            }

            this.executor = Executor.GetInstance(sso_url, rtn_url);

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
            this.executor.Redirect2Server(this.Response, this.Server);          
        }

        private TicketValidation ValidateTicket(string ticket)
        {
            TicketValidation validate_result = null;
            string rtn_json = this.executor.ValidateTicket(ticket);

            if(!string.IsNullOrEmpty(rtn_json))
            {
                validate_result = JsonConvert.DeserializeObject<TicketValidation>(rtn_json);
            }

            return validate_result;
        }
    }

    public class TicketValidation
    {
        public bool valid { get; set; }
        public string user { get; set; }
        public string newticket { get; set; }
    }
}