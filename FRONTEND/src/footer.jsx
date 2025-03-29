import React from 'react';
import { FaFacebookF, FaTwitter, FaPhone } from "react-icons/fa";

function Footer  () {
    return (
        <footer className="bg-green-600 text-white py-4">
        <div className="container mx-auto flex justify-center space-x-6">
          <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="hover:text-gray-200">
            <FaTwitter size={24} />
          </a>
          <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="hover:text-gray-200">
            <FaFacebookF size={24} />
          </a>
          <a href="tel:+33753055366" className="hover:text-gray-200">
            <FaPhone size={24} />
          </a>
        </div>
      </footer>
    );
};

export default Footer;