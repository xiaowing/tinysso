using System;
using System.Collections.Generic;
using System.Text;

namespace Tinysso.Client
{
    public class TinyssoClientException : Exception
    {
        public int Errno { get; internal set; }

        public override string Message
        {
            get
            {
                return string.Format("[TINYSSO_CL {0:D4}]{1}", this.Errno, base.Message);
            }
        }

        public TinyssoClientException(int errno, string errmsg):
            base(errmsg)
        {
            this.Errno = errno;
        }

        public TinyssoClientException(int errno, string errmsg, Exception innerException):
            base(errmsg, innerException)
        {
            this.Errno = errno;
        }

    }
}
