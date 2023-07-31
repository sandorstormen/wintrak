#!/usr/bin/bash
find backend/wintrak -type f -exec md5sum {} \; | md5sum
md5sum backend/wintrak.service