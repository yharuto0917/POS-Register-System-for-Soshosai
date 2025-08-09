"use client";

import { useState } from 'react';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { SidebarMenuButton } from '@/components/ui/sidebar'
import { ChevronRightIcon } from 'lucide-react'

export const HeaderDropdown = () => {
    const [selectStore, setSelectStore] = useState('POSレジシステムfor蒼翔祭');

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <SidebarMenuButton>
                    <img src="/soshosai.svg" alt="logo" width={24} height={24} className="h-6 w-6" />
                    <span className="text-xs">{selectStore}</span>
                    <ChevronRightIcon className="ml-auto" />
                </SidebarMenuButton>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-[--radix-popper-anchor-width]">
                <DropdownMenuItem onClick={() => setSelectStore('わたあめ')}>
                    <span>わたあめ</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSelectStore('ドリンク')}>
                    <span>ドリンク</span>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}