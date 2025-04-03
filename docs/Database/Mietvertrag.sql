CREATE TABLE [dbo].[Mietvertrag](
	[MietvertragID] [int] IDENTITY(1,1) NOT NULL,
	[MieterID] [int] NOT NULL,
	[WohnungID] [int] NOT NULL,
	[Mietbeginn] [date] NULL,
	[Mietende] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[MietvertragID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Mietvertrag]  WITH CHECK ADD FOREIGN KEY([WohnungID])
REFERENCES [dbo].[Wohnung] ([WohnungID])
GO

ALTER TABLE [dbo].[Mietvertrag]  WITH CHECK ADD FOREIGN KEY([MieterID])
REFERENCES [dbo].[Mieter] ([MieterID])