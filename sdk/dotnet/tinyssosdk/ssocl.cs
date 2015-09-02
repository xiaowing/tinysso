using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Net;
using System.Text;
using System.Web;

namespace Tinysso.Client
{
    public class Executor
    {
        private static Executor extor = null;
        private static readonly string PING_API_PATH = "api/v1.0/ping";
        private static readonly string VALIDATE_API_PATH = "api/v1.0/validation";
        private static readonly string SSO_PAGE_PATH = "sso";
        private static readonly string NEGO_TOKEN = "TSWC";
        
        private readonly string Tinysso_Server_Url = string.Empty;
        private readonly string Tinysso_Client_Returnurl = string.Empty;

        public string SsoServerUrl
        {
            get
            {
                return this.Tinysso_Server_Url;
            }
        }

        public string SsoClientUrl
        {
            get
            {
                return this.Tinysso_Client_Returnurl;
            }
        }

        private Executor(string ssosv_url, string ssocl_returnurl) 
        {
            this.Tinysso_Server_Url = ssosv_url;
            this.Tinysso_Client_Returnurl = ssocl_returnurl;

            try
            {
                if(!PingSsoServer())
                {
                    throw new TinyssoClientException(1, "Invalid request format.");
                }
            }
            catch (Exception ex)
            {
                throw new TinyssoClientException(2, "Failed to connect to Tinysso server.", ex);
            }
        }

        public static Executor GetInstance(string ssosv_url, string ssocl_returnurl)
        {
            if (extor == null)
            {
                extor = new Executor(ssosv_url, ssocl_returnurl);
            }

            return extor;
        }

        public void Redirect2Server(HttpResponse response, HttpServerUtility server)
        {
            string rtn_url = this.Tinysso_Client_Returnurl;
            string sso_url = AppendUrlWithSlash(this.Tinysso_Server_Url, Executor.SSO_PAGE_PATH);
            response.Redirect(sso_url + "?returnUrl=" + server.UrlEncode(rtn_url));
        }

        public string ValidateTicket(string ticket)
        {
            Queue<string> paramQueue = new Queue<string>();
            paramQueue.Enqueue(ticket);

            string validate_url = AppendUrlWithSlash(this.SsoServerUrl, Executor.VALIDATE_API_PATH);
            return CallGetRestfulAPI(validate_url, paramQueue);
        }

        private bool PingSsoServer()
        {
            string fullpath = AppendUrlWithSlash(this.Tinysso_Server_Url, Executor.PING_API_PATH);
            fullpath += ("?token=" + Executor.NEGO_TOKEN);

            string ret = string.Empty;
            HttpWebRequest request = WebRequest.Create(fullpath) as HttpWebRequest;
            using (HttpWebResponse response = request.GetResponse() as HttpWebResponse)
            {
                if (response.ContentType.StartsWith("text/html") &&
                    (response.StatusCode.Equals(HttpStatusCode.OK)))
                {
                    StreamReader reader = new StreamReader(response.GetResponseStream());
                    ret = reader.ReadToEnd();
                }
            }

            if (ret.Equals("OK"))
                return true;
            else
                return false;
        }

        private string CallGetRestfulAPI(string url, Queue<string> restful_parameters)
        {
            for (int i = 0; i < restful_parameters.Count; i++)
            {
                url = AppendUrlWithSlash(url, restful_parameters.Dequeue());
            }

            string rtn_json = string.Empty;
            HttpWebRequest request = WebRequest.Create(url) as HttpWebRequest;
            using (HttpWebResponse response = request.GetResponse() as HttpWebResponse)
            {
                if (response.ContentType.Equals("application/json") &&
                    (response.StatusCode.Equals(HttpStatusCode.OK)))
                {
                    StreamReader reader = new StreamReader(response.GetResponseStream());
                    rtn_json = reader.ReadToEnd();
                }
            }
            return rtn_json;
        }

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
}
